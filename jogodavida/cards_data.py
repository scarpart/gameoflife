from enums.PropertyModifier import PropertyModifier
from enums.NormalModifier import NormalModifier
from enums.ModifierType import ModifierType

# These cards will be used by the Game class. They're just here not to clutter that one.
CARDS_DATA = [
    # Salary type cards ! ! ! ! ! !  ! !
    ("Bonus", "You receive a bonus! Your salary increases by $5,000.", NormalModifier(ModifierType.SALARY, 5000), ModifierType.SALARY, 0),
    ("Demotion", "You've been demoted and your salary decreases by $7,000.", NormalModifier(ModifierType.SALARY, -7000), ModifierType.SALARY, 0),
    ("Career Change", "You've switched careers! Your salary increases by $15,000.", NormalModifier(ModifierType.SALARY, 15000), ModifierType.SALARY, 0),
    ("Overtime", "You've been working overtime! Your salary increases by $3,000.", NormalModifier(ModifierType.SALARY, 3000), ModifierType.SALARY, 0),
    ("Salary Reduction", "Company budget cuts lead to a reduction in your salary by $6,000.", NormalModifier(ModifierType.SALARY, -6000), ModifierType.SALARY, 0),
    ("Work Achievement", "Your hard work paid off! Your salary increases by $8,000.", NormalModifier(ModifierType.SALARY, 8000), ModifierType.SALARY, 0),
    ("Overtime", "You've put in some extra hours at work! Your salary increases by $3,000.", NormalModifier(ModifierType.SALARY, 3000), ModifierType.SALARY, 0),
    ("Demotion", "You've been demoted at work and your salary has been cut by $6,000.", NormalModifier(ModifierType.SALARY, -6000), ModifierType.SALARY, 0),
    ("Company Bonus", "Your company has done well and you receive a bonus of $12,000.", NormalModifier(ModifierType.SALARY, 12000), ModifierType.SALARY, 0),
    ("Bonus", "Hard work pays off! You receive a bonus of $15,000.", NormalModifier(ModifierType.SALARY, 15000), ModifierType.SALARY, 0),

    # Total money cards!!!!
    ("Debt Paid", "You were forced to pay the debt of a family member. You've lost $13,000", NormalModifier(ModifierType.TOTAL_MONEY, -13000), ModifierType.TOTAL_MONEY, 0),
    ("Car Repairs", "Your car needs major repairs. You pay $3,000.", NormalModifier(ModifierType.TOTAL_MONEY, -3000), ModifierType.TOTAL_MONEY, 0),
    ("Tax Return", "Your tax return arrived! You receive $6,000.", NormalModifier(ModifierType.TOTAL_MONEY, 6000), ModifierType.TOTAL_MONEY, 0),
    ("Investment Profit", "Your investment paid off! You earn $20,000.", NormalModifier(ModifierType.TOTAL_MONEY, 20000), ModifierType.TOTAL_MONEY, 0),
    ("Unexpected Expenses", "Life happens! You have to pay unexpected expenses of $4,000.", NormalModifier(ModifierType.TOTAL_MONEY, -4000), ModifierType.TOTAL_MONEY, 0),
    ("Broken Appliance", "Your fridge broke down and needs replacing. You pay $1,000.", NormalModifier(ModifierType.TOTAL_MONEY, -1000), ModifierType.TOTAL_MONEY, 0),
    ("Inheritance", "You've received an unexpected inheritance! You get $30,000.", NormalModifier(ModifierType.TOTAL_MONEY, 30000), ModifierType.TOTAL_MONEY, 0),
    ("Car Repairs", "Your car needed some repairs and it cost you $3,500.", NormalModifier(ModifierType.TOTAL_MONEY, -3500), ModifierType.TOTAL_MONEY, 0),
    ("Laptop Breakdown", "Your laptop broke and you need to replace it. You pay $2,000.", NormalModifier(ModifierType.TOTAL_MONEY, -2000), ModifierType.TOTAL_MONEY, 0),
    ("Antique Sale", "You sold some antiques and got $8,000.", NormalModifier(ModifierType.TOTAL_MONEY, 8000), ModifierType.TOTAL_MONEY, 0),
    ("Bad Investment Returns", "Your investments failed terribly. You've lost $20,000.", NormalModifier(ModifierType.TOTAL_MONEY, -20000), ModifierType.TOTAL_MONEY, 0),
    ("Medical Expenses", "You've had some medical expenses which cost you $10,000.", NormalModifier(ModifierType.TOTAL_MONEY, -10000), ModifierType.TOTAL_MONEY, 0),
    ("House Renovations", "You had to pay for some unexpected house renovations that cost you $15,000.", NormalModifier(ModifierType.TOTAL_MONEY, -15000), ModifierType.TOTAL_MONEY, 0),
    ("Wedding Expenses", "You helped pay for a family member's wedding. This cost you $7,000.", NormalModifier(ModifierType.TOTAL_MONEY, -7000), ModifierType.TOTAL_MONEY, 0),
    ("Legal Fees", "You had to pay some unexpected legal fees amounting to $9,000.", NormalModifier(ModifierType.TOTAL_MONEY, -9000), ModifierType.TOTAL_MONEY, 0),
    ("Lost Bet", "You lost a friendly bet and had to pay up $2,500.", NormalModifier(ModifierType.TOTAL_MONEY, -2500), ModifierType.TOTAL_MONEY, 0),
    ("Pet Surgery", "Your beloved pet needed surgery. It cost you $5,000.", NormalModifier(ModifierType.TOTAL_MONEY, -5000), ModifierType.TOTAL_MONEY, 0),
    ("Holiday Expenses", "You splurged on holiday gifts and spent $3,000.", NormalModifier(ModifierType.TOTAL_MONEY, -3000), ModifierType.TOTAL_MONEY, 0),
    ("Traffic Fines", "You had to pay a hefty amount in traffic fines. You lost $4,500.", NormalModifier(ModifierType.TOTAL_MONEY, -4500), ModifierType.TOTAL_MONEY, 0),
    ("Stock Market Loss", "The stock market took a hit and so did you. You've lost $35,000.", NormalModifier(ModifierType.TOTAL_MONEY, -35000), ModifierType.TOTAL_MONEY, 0),
    ("Identity Theft", "You fell victim to identity theft and had to cover a loss of $25,000.", NormalModifier(ModifierType.TOTAL_MONEY, -25000), ModifierType.TOTAL_MONEY, 0),

    # Property Cards !  ! ! ! !  
    ("Mountain Chalet", "A charming mountain chalet is available for purchase. Want to buy it for $21,000?", PropertyModifier(ModifierType.PROPERTY, -21000), ModifierType.PROPERTY, 0),
    ("Downtown Loft", "A loft in the heart of the city is up for grabs for $18,000. Interested?", PropertyModifier(ModifierType.PROPERTY, -18000), ModifierType.PROPERTY, 0),
    ("Desert Ranch", "A sprawling ranch in the desert is on sale for $23,000. Would you like to buy it?", PropertyModifier(ModifierType.PROPERTY, -23000), ModifierType.PROPERTY, 0),
    ("Forest Hideaway", "A secluded hideaway in the forest is available for $13,000. Ready to purchase?", PropertyModifier(ModifierType.PROPERTY, -13000), ModifierType.PROPERTY, 0),
    ("Suburban Home", "A comfortable suburban home is on the market for $16,000. Want to buy?", PropertyModifier(ModifierType.PROPERTY, -16000), ModifierType.PROPERTY, 0),
    ("Luxury Penthouse", "A luxury penthouse in the city is up for sale for $35,000! Would you like to buy it?", PropertyModifier(ModifierType.PROPERTY, -35000), ModifierType.PROPERTY, 0),
    ("Lake Cabin", "A serene cabin by the lake is available for $12,500. Interested?", PropertyModifier(ModifierType.PROPERTY, -12500), ModifierType.PROPERTY, 0),
    ("Farm Estate", "A beautiful farm estate is on the market for $22,000. Want to buy it?", PropertyModifier(ModifierType.PROPERTY, -22000), ModifierType.PROPERTY, 0),
    ("Historical Manor", "A stunning historical manor can be yours for $40,000. Ready to buy?", PropertyModifier(ModifierType.PROPERTY, -40000), ModifierType.PROPERTY, 0),
    ("Tropical Bungalow", "A bungalow in a tropical paradise is available for $28,000. Interested?", PropertyModifier(ModifierType.PROPERTY, -28000), ModifierType.PROPERTY, 0),

    # Family cards! ! ! 
    ("Marriage", "As fate would have it, you meet a woman at a bookstore. You both share a love for books and eventually decide to get married.", NormalModifier(ModifierType.FAMILY, 0, True), ModifierType.FAMILY, 1),
    ("Marriage", "After years of soul-searching, you finally meet a woman who understands you and completes you. You both decide to get married and start a life together.", NormalModifier(ModifierType.FAMILY, 0, True), ModifierType.FAMILY, 1),
    ("Marriage", "At a music festival, you meet a woman who shares your taste in music. You quickly fall in love and decide to marry.", NormalModifier(ModifierType.FAMILY, 0, True), ModifierType.FAMILY, 2),
    ("Child", "Celebrations are in order! You have a new addition to your family - a beautiful baby girl.", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 1),
    ("Child", "The stork visits your home again. You and your wife welcome a baby boy. Your family grows stronger and happier.", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 1),
    ("Child", "A blessing in disguise, your family is graced with the arrival of a new baby boy.", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 1),
    ("Child", "Life gives you a reason to celebrate again! You welcome a pair of twins, a boy and a girl, into your family.", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 1),
    ("Child", "A new journey begins as you welcome your third child into the world, a beautiful baby girl.", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 0),
    ("Child", "The joy of life doubles as you become parents to adorable twin girls!", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 1),
    ("Child", "There's a new addition to your family! A baby boy has joined your joyful journey.", NormalModifier(ModifierType.FAMILY, 0), ModifierType.FAMILY, 1)
]