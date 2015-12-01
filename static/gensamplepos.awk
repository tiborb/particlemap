#!/usr/bin/awk -f

# for i in {48740..48800}; do for j in {9247..9133}; do  echo  $j $i "$j,$i"; done ;done| ./gensamplepos.awk -v divisor=1000

BEGIN{
    if (divisor==""){divisor=1;}
    print " { \"type\": \"FeatureCollection\", \"crs\": { \"type\": \"name\", \"properties\": { \"name\": \"urn:ogc:def:crs:OGC:1.3:CRS84\" } }, \"features\": [ "
    cnt=0;
    }
{
    print "{ \"type\": \"Feature\", \"geometry\": {\"type\": \"Point\", \"coordinates\": ["$1/divisor", "$2/divisor"]}, \"properties\": {\"name\": \"" $3 "\"} }, "
}
END{  
       print "{} ] }"
}
