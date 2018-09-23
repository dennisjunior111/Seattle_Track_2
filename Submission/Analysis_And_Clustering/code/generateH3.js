const h3 = require("h3-js");
var fs = require('fs');
const args = require('minimist')(process.argv.slice(2))

const FILE = args['FILE']

const ZOOM = args['ZOOM']

let zone = require("../data/"+FILE)

for(var i=0; i<zone.length; i++){
  let record = zone[i]
  zone[i]['h3Zone'] = h3.geoToH3( record.LAT, record.LON, ZOOM)
}


fs.writeFile("../data/h3_"+FILE, JSON.stringify(zone), function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("The file was saved!");
});
