import os
import re
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.core.files import File
from django.template.defaultfilters import slugify

from category.models import Category

from downloads.models import Download


# an optparse callback function that splits a comma-separated argument
def split_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


class Command(BaseCommand):
    args = '<folder_path>'
    help = 'Adds all files on <folder_path> as downloadable files'
    option_list = BaseCommand.option_list + (
        make_option('--category',
            action='store',
            type='string',
            dest='category',
            default=None,
            help='Primary category for the downloads'),
        make_option('-r',
            action='store_true',
            dest='recursive',
            help='Recursively add files'),
        make_option('--publish',
            action='callback',
            type='string',
            callback=split_callback,
            dest='sites',
            default=False,
            help='List of comma-separated domain names to publish to'),
        )

    def handle(self, *args, **options):
        if len(args) > 0:
            category = None
            if options['category']:
                category = Category.objects.get_or_create(
                    title=options['category'],
                    slug=slugify(options['category']))[0]
            state = 'unpublished'
            sites = None
            if options['sites']:
                state = 'published'
                sites = []
                for site in options['sites']:
                    sites.append(re.escape(site))
                sites = Site.objects.filter(
                    domain__regex=r'(' + '|'.join(sites) + ')')

            count = 0
            for root, dir, files in os.walk(args[0]):
                for name in files:
                    self.stdout.write('Adding ' + root + '/' + name + '\n')
                    download = Download(title=name,
                        primary_category=category, state=state)
                    download.save()
                    for site in sites:
                        download.sites.add(site)
                    f = open(os.path.join(root, name))
                    download.file.save(name, File(f))
                    f.close()
                    count += 1
                if not options['recursive']:
                    break
            self.stdout.write('Added ' + str(count) + ' files\n')
        else:
            self.stderr.write('No folder path was specified\n')
