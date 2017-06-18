# Trollslayer [![DOI](https://zenodo.org/badge/80379199.svg)](https://zenodo.org/badge/latestdoi/80379199)
If you use this code and/or dataset (upcoming) please refer to the following works:

Dataset 1: contains annotations from a number of crowdworkers in the Trollslayer platform.
* Alvaro Garcia-Recuero, Jeff Burdges, Christian Grothoff: **Privacy-Preserving Abuse Detection in Future Decentralized Online Social Networks**. In the 11th ESORICS International Workshop on [Data Privacy Management](http://dpm2016.di.unimi.it/), 2016, Crete, Greece, [pdf](https://hal.inria.fr/hal-01355951).

## License
Copyright (C) 2015-2017
Álvaro García Recuero, algarecu@gmail.com

This file is part of the Trollslayer framework

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses>.

## Requirements (pip install):
* python-2.7.9
* sqlalchemy
* twython
* pymysql
* requests
* py-getch
* pyfiglet
* termcolor
* colorama

### Alternatively to py-getch, can install getch() for Python 2.*

* wget https://pypi.python.org/packages/source/g/getch/getch-1.0-python2.tar.gz#md5=586ea0f1f16aa094ff6a30736ba03c50
* tar xvf getch-1.0-python2.tar.gz
* cd getch-1.0
* python setup.py install

### ASCII header requires certain libraries so it prints a nice tile in the welcome screen.
* pip install colorama
* pip install termcolor
* pip install git+https://github.com/pwaller/pyfiglet

## Starting Trollslayer
+ $ python groundtruth_reader.py (It will display a message: "Loading tweets from db... please wait")
+ Next, you will prompted to enter your reviewer id. If you have one, great; else create it.
+ Once a tweet is loaded, read the guidelines below before giving ans answer on whether you consider it abusive or not.

## Using Trollslayer
### Interface
+ There are four options to mark a tweet, right(acceptable), left(abusive), up(undo), down(skip).
+ Skipping the tweet will flag it as 'unknown', which can be considered as neutral (neither positive nor negative, a blank vote).

#### Guidelines to annotate abuse: Deny, Disrupt, Degrade, Deceive (from JTRIG HUMINT Operations)
+ Deny: encouraging self-harm to others users, promoting violence (direct or indirect), terrorism or similar activities.
+ Disrupt: distracting provocations, denial-of-service, flooding with messages, promote abuse.
+ Degrade: disclosing personal and private data of others without their approval as to harm their public image/reputation.
+ Deceive: supplanting a known user identity (impersonation) for influencing other users behavior and activities,
  including assuming false identities (but not pseudonyms).

As you can see, it is easy to map the above set of guidelines to Twitter, TrollDoor, etc.
While we do not believe TrollDoor is a very good example of fighting online abuse (direct crowdsourcing to users),
their guidelines seem to resemble those of Twitter.

## Other definitions of abuse
#### [Twitter](https://support.twitter.com/articles/20169997-abusive-behavior-policy):
+ Violent threats (direct or indirect): promote violence, terrorism or similar, also to minorities or disable people, etc.
+ Abuse and harassment: sending abuse, threads, harrasing message to other user/s.
+ Self-harm: encouraging other users to commit self-harming acts is considered abuse as well.
+ Private information disclosure: to publish personal data about other users without their consent.
+ Impersonation: pretending to be someone else by registering fake accounts that expose information or similar
  meta-data from those which are a real.

#### [Trolldor](https://www.trolldor.com/faq)
+ Provocation: constructive debate holds no interest for trolls; their goal is to get attention by way of provocation.
+ Creep: users who fill other users timeline on daily basis with messages worshiping their idols, friends, relatives and
  colleagues.
+ Normally, they use “black humour” and jokes.
+ They justify abusive comments with the excuse that it is clever humour and simply misunderstood by many people.
+ It is claimed that Sly Trolls are more skilled at rhetoric.
+ They boast of being intellectually superior; although usually mistakenly. But they achieve their objective: to scare
  users less capable at answering back.
+ In the commercial world, they usually criticise a specific company or product, disguising themselves as dissatisfied
  clients or sending questions that can put whoever has to answer in a tight spot.
