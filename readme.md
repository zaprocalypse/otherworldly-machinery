
# Otherworldly Machinery

This is a tool for generating unit build images for Epic7. The idea is to show all the relevant information for units in one easy to understand place. 

**Example solo image:**

![Example solo image](https://i.ibb.co/Cm5CtKv/Challenger-Dominiel-2021-09-04-1520.png)
The advantages here are: 
* Having all item information in one place, along with the hero stats
* Details about Skill Enhancements and Imprints on the same screen as hero stats
* Much more condensed information than normal screenshots
* The ability to quickly put multiple units together without image editing 

Generally these should be a good tool if you're writing a guide for suggested stats, or alternatively for sharing your builds for advice. 

This tool **HEAVILY** relies on (the legendary) Fribbel's Epic 7 Optimizer, so [if you don't know what I'm talking about, check that out first!]((https://github.com/fribbels/Fribbels-Epic-7-Optimizer/))  

**Example group image:**

![Example group image](https://i.imgur.com/qx6MZAp.png)

Generally speaking, the goal of this tool is first to provide information, and then secondarily look good. I am not a graphics designer - so you may find it looks a bit boring - please give any suggestions for designs or feedback and I'll see what I can do. 

Currently the code is a bit (read: **very**) hacky - but in the future I'd like to make the system more customisable, and make it easier to have people make their own layouts/designs/backgrounds etc.

Also, this work is **almost entirely dependent on the work that Fribbels has done on their optimizer** - and I want to give **massive kudos and credit** to them for their work. All the data, values, calculations and stat definitions from this come directly from their work, and all I've really done is turn that data into a new format - so give them lots of kudos/support!

I'd also love to give a bunch of credit to the [EpicSevenDB.com API](https://api.epicsevendb.com/) - which is where a lot of the images and unit stat information is derived from.  Super big respect for having an open API that allows for projects like this to exist.
_________________
## Requirements
- Windows PC (Created on Windows 10, untested on earlier versions)
- Installation of [Fribbel's Optimiser](https://github.com/fribbels/Fribbels-Epic-7-Optimizer/) with game data imported
* **General warning! This is a super early release. Please be patient with bugs, weirdness, and ugliness.**
_________________
# Setting Up
![enter image description here](https://i.imgur.com/42JNhBP.png)

 1. Download the most recent release [here](https://github.com/zaprocalypse/otherworldly-machinery/releases).
 2. Extract the zip file into a folder
 3. Run Otherworldly Machinery.exe
 4. Go to the Setup Tab
 5. Click Browse in the Fribbel's Data section. 
 and find your Fribbels Optimizer autosave.json file. This file is automatically updated by Fribbels whenever you make a change within the app. On Windows, it's typically saved in your Documents Folder, under "FribbelsOptimizerSaves".
 6. Click Load Data from JSON. If you update units in Fribbels, you can click this button again to make sure Otherworldly Machinery has the updated info. The other files will come with the application, but may need to be replaced at a future time. 
_________________
# How to make an image
![](https://i.imgur.com/Dx2GKwb.png)
 1. Complete the steps in Setting Up above. If the json files are incorrectly set, everything below will fail.
 2. Make sure you have all your data up to date in Fribbels. For the most accurate images you'll want to make sure you have set:
		 - All 6 equipment slots filled (as of 0.1 it is a known issue that having any empty slots will break the app)
		 - Any imprints selected
		 - Any EE set correctly
		 - Artifact correctly set
 3. Go to the Hero Picker table. This will show a list of heroes that are in your Fribbels save. Any units that have an issue with completeness will show up in the "Reason for Issue" column.
 4. Number the units in the order you want them to show up on a multi-image. If you only want one unit in the image, just only put in one number. At the same time as building a multi-image the tool will create individual images for each unit as well. The example above was used to create the top image on this readme. 
 5. Add in the skill enhances manually next to the unit on this page.  This data is not currently tracked by Fribbel's and will need to be manually added.

![enter image description here](https://i.imgur.com/SvGrG04.png)

 6. Go to the "Output File" tab.
 7. Adjust any settings here:
	* 'Output Location' By default this is the folder named "Output" in the same place as the executable.
	* 'Show Preview' - Will automatically open the multi-image when finished
	* 'Remove App Detail Footer' - Will remove the automatically added footer that lets people know what app generated the image. You should feel free to remove this if you don't like it.
8. Press Go! button, receive image!
 _________________
## Known Issues:

* **General warning! This is a super early release. Please be willing to accept some weirdness, bugs and ugliness for now.**  It's unlikely this will do anything bad to your computer, but you may need to deal with a few problems to get it working.
* EEs are not shown on the output images. They are included in the actual stats. They will be added in the future, but are complex to show visually. 
* Some images will end up incorrectly aligned due to them appearing that way in the image sources used. I've implemented some automatic edits that should crop these to fit fairly nicely, but it's possible that it doesn't work for all units - it hasn't been tested on everyone yet
* Some artifacts or heroes may have incorrect or strange looking images. Largely these are all derived from a data source that I don't have control over, so they are difficult to fix.  
* Some newer artifacts or hero images are missing from the data sources that I use for getting the images. Unfortunately, this isn't something I can fix, and I believe is mostly caused by the encryption changes in the game making it difficult to get clean images. 
* Skill enhancements are not included in the data Fribbels captures/stores. Until this changes (which there are no plans for) - you will need to manually add these. 