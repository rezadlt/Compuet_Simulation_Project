#!/usr/bin/env python
# coding: utf-8

# In[109]:


import random
import ciw


# In[110]:


servers_number = [int(x) for x in input("Number of instances of each type of service  ").split()]
landa = int(input("The rate of entering requests into the system  "))
total_time = int(input("total time  "))
reneging_time = [int(x) for x in input("Maximum waiting time for any type of request  ").split()]

def network(servers_number):
    priority_class = [0,0,1,1,1,0,1]
    class_arrival_prob = [0.20,0.10,0.05,0.25,0.15,0.20,0.05]
    #bonus part
    error_rate_1 = lambda e: 0.02
    error_rate_2 = lambda e: 0.02
    error_rate_3 = lambda e: 0.03
    error_rate_4 = lambda e: 0.1
    error_rate_5 = lambda e: 0.2
    error_rate_6 = lambda e: 0.01
    error_rate_7 = lambda e: 0.01
    
    reneging_dist = {'Class 0': [ciw.dists.Deterministic(value=100.0) for i in range(7)],
                     'Class 1': [ciw.dists.Deterministic(value=100.0) for i in range(7)], 
                     'Class 2': [ciw.dists.Deterministic(value=100.0) for i in range(7)],
                     'Class 3': [ciw.dists.Deterministic(value=100.0) for i in range(7)],
                     'Class 4': [ciw.dists.Deterministic(value=100.0) for i in range(7)],
                     'Class 5': [ciw.dists.Deterministic(value=100.0) for i in range(7)],
                     'Class 6': [ciw.dists.Deterministic(value=100.0) for i in range(7)],
                   }
    
    service_dist = [ciw.dists.Exponential(rate = 1 / 8), 
                    ciw.dists.Exponential(rate = 1 / 5), 
                    ciw.dists.Exponential(rate = 1 / 6), 
                    ciw.dists.Exponential(rate = 1 / 9), 
                    ciw.dists.Exponential(rate = 1 / 12),
                    ciw.dists.Exponential(rate = 1 / 2), 
                    ciw.dists.Exponential(rate = 1 / 3),
                   ]
    
    arrival_dist_order_mobile = [ciw.dists.NoArrivals(),
                                 ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[0])),
                                 ciw.dists.NoArrivals(),
                                 ciw.dists.NoArrivals(),
                                 ciw.dists.NoArrivals(),
                                 ciw.dists.NoArrivals(),
                                 ciw.dists.NoArrivals(),
                                ]
    
    arrival_dist_order_web = [ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[1])),
                              ciw.dists.NoArrivals(),
                              ciw.dists.NoArrivals(),
                              ciw.dists.NoArrivals(),
                              ciw.dists.NoArrivals(),
                              ciw.dists.NoArrivals(),
                              ciw.dists.NoArrivals(),
                             ]
    
    arrival_dist_sendmessage_todelivery = [ciw.dists.NoArrivals(),
                                           ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[2])),
                                           ciw.dists.NoArrivals(),
                                           ciw.dists.NoArrivals(),
                                           ciw.dists.NoArrivals(),
                                           ciw.dists.NoArrivals(),
                                           ciw.dists.NoArrivals(),
                                          ]
    
    arrival_dist_info_mobile = [ciw.dists.NoArrivals(),
                                ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[3])),
                                ciw.dists.NoArrivals(),
                                ciw.dists.NoArrivals(),
                                ciw.dists.NoArrivals(),
                                ciw.dists.NoArrivals(),
                                ciw.dists.NoArrivals(),
                               ]
    
    arrival_dist_info_web = [ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[4])),
                             ciw.dists.NoArrivals(),
                             ciw.dists.NoArrivals(),
                             ciw.dists.NoArrivals(),
                             ciw.dists.NoArrivals(),
                             ciw.dists.NoArrivals(),
                             ciw.dists.NoArrivals(),
                            ]
    
    arrival_dist_courier_request = [ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[5])),
                                    ciw.dists.NoArrivals(),
                                    ciw.dists.NoArrivals(),
                                    ciw.dists.NoArrivals(),
                                    ciw.dists.NoArrivals(),
                                    ciw.dists.NoArrivals(),
                                    ciw.dists.NoArrivals(),
                                   ]
    
    arrival_dist_order_tracking = [ciw.dists.NoArrivals(),
                                   ciw.dists.Exponential(rate=1/(landa*class_arrival_prob[6])),
                                   ciw.dists.NoArrivals(),
                                   ciw.dists.NoArrivals(),
                                   ciw.dists.NoArrivals(),
                                   ciw.dists.NoArrivals(),
                                   ciw.dists.NoArrivals(),
                                  ]
    
    rout_dist_order_mobile = [[0,0,0,0,0,0,0],
                              [0,0,0,0,1,0,0],
                              [0,0,0,0,0,0,0],
                              [0,0,1,0,0,0,0],
                              [0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0]]
    
    rout_dist_order_web = [[0,0,0,0,1,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,1,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0]]
    
    rout_dist_sendmessage_todelivery = [[0,0,0,0,0,0,0],
                                        [0,0,0,0,0,1,0],
                                        [0,0,0,0,0,0,0],
                                        [0,0,0,0,0,0,0],
                                        [0,0,0,1,0,0,0],
                                        [0,0,0,0,0,0,0]]
    
    rout_dist_info_mobile = [[0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,1],
                             [0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0],
                             [0,0,0,1,0,0,0],
                             [0,0,0,0,0,0,0]]
    
    rout_dist_info_web = [[0,0,0,0,0,0,1],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,1,0,0,0],
                           [0,0,0,0,0,0,0]]
    
    rout_dist_courier_request = [[0,0,0,0,0,0,1],
                                 [0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0],
                                 [0,0,0,1,0,0,0]]
    
    rout_dist_order_tracking = [[0,0,0,0,0,0,0],
                                [0,0,0,0,1,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0]]
    
    N = ciw.create_network(
        arrival_distributions = {'Class 0': arrival_dist_info_mobile,
                                 'Class 1': arrival_dist_order_web,
                                 'Class 2': arrival_dist_sendmessage_todelivery,
                                 'Class 3': arrival_dist_info_mobile,
                                 'Class 4': arrival_dist_info_web,
                                 'Class 5': arrival_dist_courier_request,
                                 'Class 6': arrival_dist_order_tracking,
                                },
        
        service_distributions = {'Class 0': service_dist,
                                 'Class 1': service_dist,
                                 'Class 2': service_dist,
                                 'Class 3': service_dist,
                                 'Class 4': service_dist,
                                 'Class 5': service_dist,
                                 'Class 6': service_dist,
                                },
        
        baulking_functions = {'Class 0': [error_rate_1 for i in range(7)],
                              'Class 1': [error_rate_2 for i in range(7)],
                              'Class 2': [error_rate_3 for i in range(7)],
                              'Class 3': [error_rate_4 for i in range(7)],
                              'Class 4': [error_rate_5 for i in range(7)],
                              'Class 5': [error_rate_6 for i in range(7)],
                              'Class 6': [error_rate_7 for i in range(7)],
                             },
        
        routing = {'Class 0': rout_dist_order_mobile,
                   'Class 1': rout_dist_order_web,
                   'Class 2': rout_dist_sendmessage_todelivery,
                   'Class 3': rout_dist_info_mobile,
                   'Class 4': rout_dist_info_web,
                   'Class 5': rout_dist_courier_request,
                   'Class 6': rout_dist_order_tracking,
                  },
        number_of_servers = servers_number,
        
        priority_classes = {'Class 0': priority_class[0],
                            'Class 1': priority_class[1],
                            'Class 2': priority_class[2],
                            'Class 3': priority_class[3],
                            'Class 4': priority_class[4],
                            'Class 5': priority_class[5],
                            'Class 6': priority_class[6],
                           },
        reneging_time_distributions = reneging_time,
        
    )
    return N                      


# In[111]:


def get_queue_length_mean(recs, Node):
    queue_sizes = list()
    for rec in recs:
        if rec.node == Node:
            queue_sizes.append(rec.queue_size_at_arrival)
    if len(queue_sizes) == 0:
        return 0
    x = sum(queue_sizes) / len(queue_sizes)
    return x

def wait_in_queue_mean(recs):
    wait_times = [[] for rec in range(7)]
    for rec in recs:
        wait_times[recs.customer_class].append(rec.waiting_time)
    class_wait_times = []
    for rec in range(7):
        y = sum(wait_times[i]
        class_wait_times.append(y) / len(wait_times[i]))
    x = 0
    for i in wait_times:
        x += len(i)
    all_mean_wait_time = sum(sum(wait_times, [])) / x
    return class_wait_times, all_mean_wait_time

def get_node_util(recs, node_id, node_number, total_time):
    util_time = 0
    for rec in recs:
        if rec.node == node_id and rec.service_time > 0:
            util_time += rec.service_time
    x = util_time / total_time
    x = x / node_number
    return x

def get_reneged_requests(id_rec_dict, total_customers: list):
    reneged_requests = [0] * 7
    for id_number in id_rec_dict:
        if id_rec_dict[id_number][0].record_type == "renege":
            reneged_requests[id_rec_dict[id_number][0].customer_class] += 1
    for i in range(7):
        reneged_requests[i] = reneged_requests[i] / total_customers[i]
    x = sum(baulked_class)
    y = sum(total_customers)
    all_mean_baulked_class = x / y
    return baulked_class, all_mean_baulked_class 


# In[112]:


for i in range (0,7):
    print("queue length is:  ", i, " ", get_queue_length_mean(recs, i))
    print("node util is  " ,get_node_util(recs, i, servers_number[i -1], total_time))
class_wait_times, all_mean_wait_time = wait_in_queue_mean(recs)
print("class wait times:  " ,class_wait_time)
reneged_request, all_mean_reneged_requests = get_reneged_requests(id_rec_dict, total_customers)
print("reneged requests:  ", reneged_requests)
print("all mean reneged requests:  ", all_mean_reneged_requests)
baulked_class, all_mean_baulked_class = get_baulked_class(Q.baulked_dict, total_customers)
print("baulked class:  ", baulked_class)
print("all mean baulked class:  ", all_mean_baulked_class)

