import random
from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand
from django_seed import Seed
from lists.models import List
from users.models import User
from rooms.models import Room


class Command(BaseCommand):

    help = "This command creates lists"

    def add_arguments(self, parser):

        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many lists do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()
        all_rooms = Room.objects.all()
        seeder.add_entity(
            List,
            number,
            {
                "name": lambda x: seeder.faker.name(),
                "user": lambda x: random.choice(all_users),
            },
        )
        created_lists = seeder.execute()
        cleaned_lists = flatten(created_lists.values())
        for pk in cleaned_lists:
            list_model = List.objects.get(pk=pk)
            to_add = all_rooms[random.randint(0, 5) : random.randint(6, 20)]
            list_model.rooms.add(*to_add)  # * is like doing 'random.choice'
        self.stdout.write(self.style.SUCCESS(f" {number} Lists Created ✨"))
