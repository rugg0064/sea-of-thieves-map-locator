# sea-of-thieves-map-locator
A set of scripts to determine the location of treasure maps in Sea of Thieves so that you don't need to memorize the dozens of islands or search across the map.

createContrasts.py takes images scraped from https://maps.seaofthieves.rarethief.com/ and creates contrasts saved to another folder.

Then, scanImage.py will process a given file and compare them to the contrasts, printing out the one it thinks best fits from the contrasts.

When running these scripts, ensure the working directory is the root folder of this repository.