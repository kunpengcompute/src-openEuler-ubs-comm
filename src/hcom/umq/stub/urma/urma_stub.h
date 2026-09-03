/*
 * SPDX-License-Identifier: MIT
 * Copyright (c) Huawei Technologies Co., Ltd. 2026-2026. All rights reserved.
 * Description: stub for urma
 * Create: 2026
 */

#ifndef URMA_STUB_H
#define URMA_STUB_H

#include <stdint.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdbool.h>

typedef void* urma_device_t;
typedef void* urma_eid_t;

int urma_init(void);
void urma_cleanup(void);
urma_device_t urma_get_device(const char* name);
urma_eid_t urma_get_eid(urma_device_t dev, const char* addr);

int urma_common_init(void);
void urma_common_cleanup(void);
int urma_get_version(void);
void* urma_common_alloc(size_t size);
void urma_common_free(void* ptr);

#define UVS_MAX_ROUTES 16
#define UVS_EID_SIZE                 (16)

typedef union uvs_eid {
    uint8_t raw[UVS_EID_SIZE];      // Network Order
    struct {
        uint64_t reserved;          // If IPv4 mapped to IPv6, == 0
        uint32_t prefix;            // If IPv4 mapped to IPv6, == 0x0000ffff
        uint32_t addr;              // If IPv4 mapped to IPv6, == IPv4 addr
    } in4;
    struct {
        uint64_t subnet_prefix;
        uint64_t interface_id;
    } in6;
} uvs_eid_t;

typedef union uvs_route_flag {
    struct {
        uint32_t rtp : 1;
        uint32_t ctp : 1;
        uint32_t utp : 1;
        uint32_t reserved : 29;
    } bs;
    uint32_t value;
} uvs_route_flag_t;

typedef struct uvs_route {
    uvs_eid_t src;
    uvs_eid_t dst;
    uvs_route_flag_t flag;
    uint32_t hops;      // Only supports direct routes, currently 0.
    uint32_t chip_id;
} uvs_route_t;

typedef struct uvs_route_list {
    uint32_t len;
    uvs_route_t buf[UVS_MAX_ROUTES];
} uvs_route_list_t;

/**
 * UVS set topo info which gets from MXE module.
 * @param[in] topo: topo info of one bonding device
 * @param[in] topo_num: number of bonding devices
 * Return: 0 on success, other value on error
 */
int uvs_set_topo_info(void *topo, uint32_t topo_num);

/**
 * Get primary and port eid from topo info.
 * @param[in] route: parameter that contains src_v_eid and dst_v_eid,
 *                          refers to uvs_route_t;
 * @param[out] route_list: a list buffer, containing all routes returned;
 * Return: 0 on success, other value on error
 */

int uvs_get_route_list(const uvs_route_t *route, uvs_route_list_t *route_list);
 	 
#endif