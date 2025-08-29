  ______   ______   ___   ____  _____ _ ___
 / _ \  \ /  / _ \ / __| / __| / __  |  _  \ 
|  __/ >    < (_) |\__ \/ (__ | (__) | / \  |
 \___/__/ \__\___/ |___/\____| \_____|_|  |_|
________________________________________________
A tool to scan for configuration weaknesses in Exoscale Cloud. 

As of now, only Windows is supported, that has something to do with the paths. Fixing it as soon as I have time ;)

To run it, create an API-Key that has permissions to list all objects and create the following environment variables: 
EXOSCALE_API_KEY
EXOSCALE_API_SECRET

As every organization has a different understanding of thresholds and when a resource is "deprecated" or "outdated", you can change those thresholds in the respective controls: 
 - OldInstanceAge: 90
 - SameRegionThreshold: 75%
 - LargeIPBlocks: /24

If you want to use Shodan capabilities, set the environment variable SHODAN_API_KEY. Else, the controls are skipped. 

This is a work in progress, so more controls will be added, and all things are subject to change. 
