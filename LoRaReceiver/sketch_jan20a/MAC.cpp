#include "MAC.h"
#include <stdint.h>

const NodeDef nodeDefs[] = {
    { "48:CA:43:B6:EE:2C", 1 },
    { "77:88:99:AA:BB:CC", 2 }
  };

const char masterNode[18] = "48:CA:43:B6:A8:0C";  


const int NUM_NODES = sizeof(nodeDefs) / sizeof(NodeDef);