from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import *

engine = create_engine('postgresql://sakr:SSaa1219@localhost/itemsCatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# categories
Category1 = Category(name="Cats1",
                      user_id=1)
session.add(Category1)
session.commit()

Category2 = Category(name="Cats2",
                      user_id=2)
session.add(Category2)
session.commit

Category3 = Category(name="Cats3",
                      user_id=1)
session.add(Category3)
session.commit()

Category4 = Category(name="Cats4",
                      user_id=1)
session.add(Category4)
session.commit()

Category5 = Category(name="Cats5",
                      user_id=1)
session.add(Category5)
session.commit()

#items
Item1 = Items(name="lola",
               date=datetime.datetime.now(),
               description="lola is very clever.",
               picture="https://theme.zdassets.com/theme_assets/578885/58cfe94f15a47601d98ff855ee938d32653788c3.png",
               category_id=1,
               user_id=1)
session.add(Item1)
session.commit()

Item2 = Items(name="Shirt",
               date=datetime.datetime.now(),
               description="Shirt for me.",
               picture="https://studentaffairscollective.org/wp-content/uploads/2016/06/feature1-1.png",
               category_id=1,
               user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(name="selfe",
               date=datetime.datetime.now(),
               description="selfe is fantastic.",
               picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSej7eak9-o5r8QHDhpdbu4dZRCUyMRXi83emvw-rbVdizx-tA1",
               category_id=1,
               user_id=1)
session.add(Item3)
session.commit()

print "Doneee..."
