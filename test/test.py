from pycubex_parser import CubexParser

def main():
    cubex_file_path = "data/blast.p64.r1/profile.cubex"
    with CubexParser(cubex_file_path) as cubex:

        metrics = cubex.get_metrics()
        print(metrics[1])
        metric_values = cubex.get_metric_values(metric=metrics[1])
        #print(metric_values)
        cnode = cubex.get_cnode(metric_values.cnode_indices[0])
        print(cnode)


        for metric in cubex.get_metrics():
            #print("Metric:",metric)

            metric_values = cubex.get_metric_values(metric=metric)
            cnode = cubex.get_cnode(metric_values.cnode_indices[0])
            region = cubex.get_region(cnode)
            #print(region)
            cnode_values = metric_values.cnode_values(cnode.id)
            #print(cnode_values)

if __name__ == "__main__":
    main()