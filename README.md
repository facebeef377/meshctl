#meshctl.py

A wrapper for meshctl utility.

###Dependency

You need BT 4.0 or higher and BlueZ 5.49 or higher.

####Install BlueZ

/TODO install flask, pip, etc...

xxxxxxxxxx sudo apt-get updatesudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-devgit clone https://git.kernel.org/pub/scm/bluetooth/bluez.gitcd bluez$ bootstrap$ ./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var --enable-mesh$ make$ sudo make install

###Install 

After installing blueZ put files from this repository to `/mesh`

Data from`html` put into apache2 data folder. 

###Basic Run

`sudo python meshctl.py`

Next open `127.0.0.1` in your browser and login with `usr:zaq`

##Api

//TODO
