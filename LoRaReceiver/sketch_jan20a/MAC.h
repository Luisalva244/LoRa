#ifndef MAC_H
#define MAC_H

#include <stdint.h>

struct NodeDef {
    const char *mac;
    uint8_t nodeId;
};

extern const NodeDef nodeDefs[];
extern const int NUM_NODES;

#endif