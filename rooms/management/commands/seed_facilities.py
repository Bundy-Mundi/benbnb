from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    # If you wanna create commands arguments try:

    """ 
        def add_arguments(self, parser):

            parser.add_argument(
                "--success", action="store_true", help="This is a custom command"
            )
    """

    help = "This command creates facilities"

    def handle(self, *args, **options):

        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} Facilites Created ✨"))

