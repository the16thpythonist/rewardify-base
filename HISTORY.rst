=======
History
=======

0.0.0 (2019-06-08)
------------------

* First release on PyPI.

0.1.0 (2019-06-14)
------------------

* Initial version

0.1.1 (2019-06-14)
------------------

* Fixed bug in setup.py, which caused the "backends" package to be excluded

0.2.0 (2019-06-15)
------------------

* Internal changes in the recycle method for rewards
* Added a "user_exists" method to the facade, which will return, whether or not the given user
  name exists in the database or not
* Added "effect" field to Reward class
    * An optional string item "effect" can ba added to the config of any reward. This string should contain
      special syntax, for what effect the reward usage should have on the rewardify system
    * Currently granting the user gold and dust are supported effects
* Added more methods for handling rewards to the facade, which include buying, using and recycling
  rewards

0.2.1 (2019-06-16)
------------------

* Fixed, that the facade method for buying a pack internally called the method for adding a pack, thus not
  actually spending gold on it

0.2.2 (2019-06-16)
------------------

* Added "user.save()" calls to all the methods of the facade, that modify the models, so that the modifications
actually get taken over into the database
