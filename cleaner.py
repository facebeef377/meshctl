uno="""{
  "$schema":"file:\/\/\/BlueZ\/Mesh\/local_schema\/mesh.jsonschema",
  "meshName":"BT Mesh",
  "netKeys":[
    {
      "index": 0,
      "keyRefresh": 0
    }
  ],
  "appKeys":[
    {
      "index": 0,
      "boundNetKey": 0
    },
    {
      "index": 1,
      "boundNetKey": 0
    }
  ],
"node": {
	"IVindex":"00000005",
	"IVupdate":"0",
	"sequenceNumber": 0,
    "composition": {
        "cid": "0002",
        "pid": "0010",
        "vid": "0001",
        "crpl": "000a",
        "features": {
            "relay": false,
            "proxy": true,
            "friend": false,
            "lowPower": false
        },
        "elements": [
            {
                "elementIndex": 0,
                "location": "0001",
                "models": ["0000", "0001", "1001"]
            }
        ]
    },
    "configuration":{
        "netKeys": [0],
        "appKeys": [ 0, 1],
        "defaultTTL": 10,
        "elements": [
          {
            "elementIndex": 0,
            "unicastAddress":"0077",
            "models": [
               {
                 "modelId": "1001",
                 "bind": [1]
                }
            ]
          }
        ]
    }
  }
}
"""
dos="""{
  "$schema":"file:\/\/\/BlueZ\/Mesh\/schema\/mesh.jsonschema",
  "meshName":"BT Mesh",
  "IVindex":5,
  "IVupdate":0,
  "netKeys":[
    {
      "index":0,
      "keyRefresh":0,
      "key":"18eed9c2a56add85049ffc3c59ad0e12"
    }
  ],
  "appKeys":[
    {
      "index":0,
      "boundNetKey":0,
      "key":"4f68ad85d9f48ac8589df665b6b49b8a"
    },
    {
      "index":1,
      "boundNetKey":0,
      "key":"2aa2a6ded5a0798ceab5787ca3ae39fc"
    }
  ],
  "provisioners":[
    {
      "provisionerName":"BT Mesh Provisioner",
      "unicastAddress":"0077",
      "allocatedUnicastRange":[
        {
          "lowAddress":"0100",
          "highAddress":"7fff"
        }
      ]
    }
  ],
}
"""

def clean():
	print "Ja tu tylko sprzatam..."
	pliczor=open("local_node.json",'w')
	pliczor.write(uno)
	pliczor.close()
	pliczor=open("prov_db.json",'w')
	pliczor.write(dos)
	pliczor.close()
	print "Gitara siema"

clean()