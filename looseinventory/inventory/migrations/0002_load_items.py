from django.db import migrations


ITEMS_BY_SET = {
    "Leather": ["Leather Helm", "Leather Armor", "Leather Boots", "Leather Gloves", "Leather Pants"],
    "Pad": ["Pad Helm", "Pad Armor", "Pad Boots", "Pad Gloves", "Pad Pants"],
    "Vine": ["Vine Helm", "Vine Armor", "Vine Boots", "Vine Gloves", "Vine Pants"],
    "Bronze": ["Bronze Helm", "Bronze Armor", "Bronze Boots", "Bronze Gloves", "Bronze Pants"],
    "Silk": ["Silk Helm", "Silk Armor", "Silk Boots", "Silk Gloves", "Silk Pants"],
    "Bone": ["Bone Helm", "Bone Armor", "Bone Boots", "Bone Gloves", "Bone Pants"],
    "Scale": ["Scale Helm", "Scale Armor", "Scale Boots", "Scale Gloves", "Scale Pants"],
    "Wind": ["Wind Helm", "Wind Armor", "Wind Boots", "Wind Gloves", "Wind Pants"],
    "Violent Wind": ["Violent Wind Helm", "Violent Wind Armor", "Violent Wind Boots", "Violent Wind Gloves", "Violent Wind Pants"],
    "Sphinx": ["Sphinx Helm", "Sphinx Armor", "Sphinx Boots", "Sphinx Gloves", "Sphinx Pants"],
    "Brass": ["Brass Helm", "Brass Armor", "Brass Boots", "Brass Gloves", "Brass Pants"],
    "Spirit": ["Spirit Helm", "Spirit Armor", "Spirit Boots", "Spirit Gloves", "Spirit Pants"],
    "Plate": ["Plate Helm", "Plate Armor", "Plate Boots", "Plate Gloves", "Plate Pants"],
    "Legendary": ["Legendary Helm", "Legendary Armor", "Legendary Boots", "Legendary Gloves", "Legendary Pants"],
    "Red Winged": ["Red Winged Helm", "Red Winged Armor", "Red Winged Boots", "Red Winged Gloves", "Red Winged Pants"],
    "Guardian": ["Guardian Helm", "Guardian Armor", "Guardian Boots", "Guardian Gloves", "Guardian Pants"],
    "Dragon Set": ["Dragon Set Helm", "Dragon Set Armor", "Dragon Set Boots", "Dragon Set Gloves", "Dragon Set Pants"],
    "Light Plate": ["Light Plate Helm", "Light Plate Armor", "Light Plate Boots", "Light Plate Gloves", "Light Plate Pants"],
    "Sacred Fire": ["Sacred Fire Helm", "Sacred Fire Armor", "Sacred Fire Boots", "Sacred Fire Pants"],
    "Ancient Set": ["Ancient Set Helm", "Ancient Set Armor", "Ancient Set Boots", "Ancient Set Gloves", "Ancient Set Pants"],
    "Adamantine": ["Adamantine Helm", "Adamantine Armor", "Adamantine Boots", "Adamantine Gloves", "Adamantine Pants"],
    "Storm Crow": ["Storm Crow Armor", "Storm Crow Boots", "Storm Crow Gloves", "Storm Crow Pants"],
    "Storm Zahard": ["Storm Zahard Helm", "Storm Zahard Armor", "Storm Zahard Boots", "Storm Zahard Pants"],
    "Black Dragon": ["Black Dragon Helm", "Black Dragon Armor", "Black Dragon Boots", "Black Dragon Gloves", "Black Dragon Pants"],
    "Demonic": ["Demonic Helm", "Demonic Armor", "Demonic Boots", "Demonic Gloves", "Demonic Pants"],
    "Grand Soul": ["Grand Soul Helm", "Grand Soul Armor", "Grand Soul Boots", "Grand Soul Gloves", "Grand Soul Pants"],
    "Holy Spirit": ["Holy Spirit Helm", "Holy Spirit Armor", "Holy Spirit Boots", "Holy Spirit Gloves", "Holy Spirit Pants"],
    "Dark Steel": ["Dark Steel Helm", "Dark Steel Armor", "Dark Steel Boots", "Dark Steel Gloves", "Dark Steel Pants"],
    "Dark Phoenix": ["Dark Phoenix Helm", "Dark Phoenix Armor", "Dark Phoenix Boots", "Dark Phoenix Gloves", "Dark Phoenix Pants"],
    "Thunder Hawk": ["Thunder Hawk Armor", "Thunder Hawk Boots", "Thunder Hawk Gloves", "Thunder Hawk Pants"],
    "Great Dragon": ["Great Dragon Helm", "Great Dragon Armor", "Great Dragon Boots", "Great Dragon Gloves", "Great Dragon Pants"],
    "Dark Soul": ["Dark Soul Helm", "Dark Soul Armor", "Dark Soul Boots", "Dark Soul Gloves", "Dark Soul Pants"],
    "Hurricane": ["Hurricane Armor", "Hurricane Boots", "Hurricane Gloves", "Hurricane Pants"],
    "Red Spirit": ["Red Spirit Helm", "Red Spirit Armor", "Red Spirit Boots", "Red Spirit Gloves", "Red Spirit Pants"],
    "Dark Master": ["Dark Master Helm", "Dark Master Armor", "Dark Master Boots", "Dark Master Gloves", "Dark Master Pants"],
    "Storm Blitz": ["Storm Blitz Helm", "Storm Blitz Armor", "Storm Blitz Boots", "Storm Blitz Gloves", "Storm Blitz Pants"],
    "Piercing Grove": ["Piercing Grove Helm", "Piercing Grove Armor", "Piercing Grove Boots", "Piercing Grove Pants"],
    "Dragon Knight": ["Dragon Knight Helm", "Dragon Knight Armor", "Dragon Knight Boots", "Dragon Knight Gloves", "Dragon Knight Pants"],
    "Venom Mist": ["Venom Mist Helm", "Venom Mist Armor", "Venom Mist Boots", "Venom Mist Gloves", "Venom Mist Pants"],
    "Sylphid Ray": ["Sylphid Ray Helm", "Sylphid Ray Armor", "Sylphid Ray Boots", "Sylphid Ray Gloves", "Sylphid Ray Pants"],
    "Volcano": ["Volcano Armor", "Volcano Boots", "Volcano Gloves", "Volcano Pants"],
    "Sunlight": ["Sunlight Helm", "Sunlight Armor", "Sunlight Boots", "Sunlight Gloves", "Sunlight Pants"],
    "Succubus": ["Succubus Helm", "Succubus Armor", "Succubus Boots", "Succubus Gloves", "Succubus Pants"],
    "Phoenix Soul": ["Phoenix Soul Helm", "Phoenix Soul Armor", "Phoenix Soul Boots", "Phoenix Soul Pants"],
}


def load_items(apps, schema_editor):
    Item = apps.get_model("inventory", "Item")

    items_to_create = []

    for item_list in ITEMS_BY_SET.values():
        for item_name in item_list:
            items_to_create.append(Item(name=item_name))

    # evita erro se rodar duas vezes
    Item.objects.bulk_create(
        items_to_create,
        ignore_conflicts=True,
    )


def reverse_load_items(apps, schema_editor):
    Item = apps.get_model("inventory", "Item")

    all_item_names = [
        item_name
        for item_list in ITEMS_BY_SET.values()
        for item_name in item_list
    ]

    Item.objects.filter(name__in=all_item_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_items, reverse_load_items),
    ]
