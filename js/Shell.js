(function (nx) {
    /**
     * define application
     */
    var topologyData = {
        nodes: [
            {"id": 0, "x": 380, "y": 25, "name": "nx9kv"},
            {"id": 1, "x": 280, "y": 25, "name": "nx9kv"},
            {"id": 2, "x": 328, "y": 1, "name": "cloud"},

            {"id": 3, "x": 270, "y": 57, "name": "router1"},
            {"id": 4, "x": 392, "y": 57, "name": "router2"},

            {"id": 5, "x": 218, "y": 57, "name": "switch1"},
            {"id": 6, "x": 218, "y": 93, "name": "switch2"},
            {"id": 7, "x": 270, "y": 93, "name": "switch3"},
            {"id": 8, "x": 441, "y": 57, "name": "switch4"},
            {"id": 9, "x": 441, "y": 93, "name": "switch5"},
            {"id": 10, "x": 395, "y": 93, "name": "switch6"},

            {"id": 11, "x": 188, "y": 37, "name": "pc1"},
            {"id": 12, "x": 188, "y": 57, "name": "pc2"},
            {"id": 13, "x": 188, "y": 77, "name": "pc3"},
            {"id": 14, "x": 188, "y": 100, "name": "pc4"},
            {"id": 15, "x": 188, "y": 122, "name": "pc5"},
            {"id": 16, "x": 218, "y": 122, "name": "pc6"},
            {"id": 17, "x": 253, "y": 122, "name": "pc7"},
            {"id": 18, "x": 280, "y": 122, "name": "pc8"},
            {"id": 19, "x": 308, "y": 122, "name": "pc9"},

            {"id": 20, "x": 475, "y": 37, "name": "pc10"},
            {"id": 21, "x": 475, "y": 57, "name": "pc11"},
            {"id": 22, "x": 475, "y": 77, "name": "pc12"},
            {"id": 23, "x": 475, "y": 100, "name": "pc13"},
            {"id": 24, "x": 475, "y": 122, "name": "pc14"},
            {"id": 25, "x": 445, "y": 122, "name": "pc15"},
            {"id": 26, "x": 412, "y": 122, "name": "pc16"},
            {"id": 27, "x": 385, "y": 122, "name": "pc17"},
            {"id": 28, "x": 358, "y": 122, "name": "pc18"},



        ],
        links: [
            {"source": 0, "target": 2},
            {"source": 1, "target": 2},
            {"source": 0, "target": 1},
            {"source": 1, "target": 0},
            {"source": 3, "target": 0},
            {"source": 3, "target": 1},
            {"source": 4, "target": 0},
            {"source": 4, "target": 1},
            {"source": 5, "target": 3},
            {"source": 6, "target": 3},
            {"source": 7, "target": 3},
            {"source": 8, "target": 4},
            {"source": 9, "target": 4},
            {"source": 10, "target": 4},
            {"source": 11, "target": 5},
            {"source": 12, "target": 5},
            {"source": 13, "target": 5},
            {"source": 14, "target": 6},
            {"source": 15, "target": 6},
            {"source": 16, "target": 6},
            {"source": 17, "target": 7},
            {"source": 18, "target": 7},
            {"source": 19, "target": 7},
            {"source": 20, "target": 8},
            {"source": 21, "target": 8},
            {"source": 22, "target": 8},
            {"source": 23, "target": 9},
            {"source": 24, "target": 9},
            {"source": 25, "target": 9},
            {"source": 26, "target": 10},
            {"source": 27, "target": 10},
            {"source": 28, "target": 10},

        ]
    };

    var Shell = nx.define(nx.ui.Application, {
        properties: {
            icon: {
                value: function() {
                    return function(vertex) {
                        var id = vertex.get("id");
                        if (id < 2) {
                            return 'nexus5000'
                        }
                        else if(id==2){
                            return 'cloud'
                        }
                        else if(id>=3&&id<=4){
                            return 'router'
                        }
                        else if(id>=5&&id<=10){
                            return'switch'
                        }
                        else{
                            return 'host'
                        }
                    }
                }
            }
        },
        methods: {
            start: function () {
                //your application main entry

                // initialize a topology
                var topo = new nx.graphic.Topology({
                    // set the topology view's with and height
                    width: 1150,
                    height: 660,
                    // node config
                    nodeConfig: {
                        // label display name from of node's model, could change to 'model.id' to show id
                        label: 'model.name',
                        iconType: '{#icon}'
                    },
                    // link config
                    linkConfig: {
                        // multiple link type is curve, could change to 'parallel' to use parallel link
                        linkType: 'curve'
                    },
                    nodeSetConfig:{
                      iconType: 'model.deice_type'
                    },
                    // show node's icon, could change to false to show dot
                    showIcon: true
                });

                //set data to topology
                topo.data(topologyData);
                //attach topology to document
                topo.attach(this);
            }
        }
    });
    /**
     * create application instance
     */
    var shell = new Shell();

    /**
     * invoke start method
     */
    shell.start();
})(nx);