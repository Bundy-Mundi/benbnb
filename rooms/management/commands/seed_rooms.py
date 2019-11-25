import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule
from users.models import User


class Command(BaseCommand):

    help = "This command creates rooms"

    def add_arguments(self, parser):

        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()
        all_room_types = RoomType.objects.all()
        all_amenities = Amenity.objects.all()
        all_facilities = Facility.objects.all()
        all_house_rules = HouseRule.objects.all()
        my_word_list = [
            "danish",
            "cheesecake",
            "sugar",
            "Lollipop",
            "wafer",
            "Gummies",
            "sesame",
            "Jelly",
            "beans",
            "pie",
            "bar",
            "Ice",
            "oat",
        ]
        seeder.add_entity(
            Room,
            number,
            {
                # 'fields' of AbstractUser
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(all_room_types),
                "price": lambda x: random.randint(20, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 7),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        for pk in created_clean:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                Photo.objects.create(
                    name=seeder.faker.sentence(ext_word_list=my_word_list),
                    caption=seeder.faker.sentence(),
                    file=f"room_photos/{random.randint(1,31)}.webp",
                    room=room,
                )
            for a in all_amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in all_facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in all_house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f" {number} Rooms Created ✨"))

