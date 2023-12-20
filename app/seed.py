from app import app

from app import db, Hero, Power, HeroPower

with app.app_context():

    # Create sample heroes
    hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
    hero3 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

    db.session.add_all([hero1, hero2, hero3])
    db.session.commit()

    # Create sample powers
    power1 = Power(name="Super Strength", description="Gives the wielder super-human strengths")
    power2 = Power(name="Flight", description="Gives the wielder the ability to fly through the skies at supersonic speed")

    db.session.add_all([power1, power2])
    db.session.commit()

    # Associate powers with heroes
    hero_power1 = HeroPower(hero_id=1, power_id=1, strength="Strong")
    hero_power2 = HeroPower(hero_id=1, power_id=2, strength="Average")
    hero_power3 = HeroPower(hero_id=2, power_id=1, strength="Weak")

    db.session.add_all([hero_power1, hero_power2, hero_power3])
    db.session.commit()

