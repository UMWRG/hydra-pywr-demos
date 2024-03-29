import hydra_functions as hf
import pandas as pd
import click

plt = None

try:
    import matplotlib.pyplot as plt
except ImportError:
    print ("You must install matplotlib to enable plotting. Try pip install matplotlib.")

@click.command()
@click.option('--scenario-id', '-s', help='Scenario ID')
@click.option('--attribute-name', '-a', help='The name of the attribute to plot.')
@click.option('--username', '-u', default='root', help='The requesting users username')
@click.option('--password', '-p', default='', help='The requesting users password')
def plot_results(scenario_id, attribute_name, username, password):
    """
        Get the details for a network
    """
    #Don't proceed if matplotlib is not installed
    if plt == None:
        return

    #Connect to hydra
    conn = hf.connect(username, password)
    
    #make a lookup of the ID of all attributes to their name so we can look it up
    all_attributes = conn.get_attributes()
    attribute_id_name_map = {}
    for a in all_attributes:
        attribute_id_name_map[a.id] = a.name
    
    datasets_to_plot = {}

    try:
        #Get all the datasets matching the specified attribute
        scenario = conn.get_scenario(scenario_id=scenario_id)

        network = conn.get_network(network_id=scenario.network_id)


        node_ra_map = {}

        for node in network.nodes:
            for ra in node.attributes:
                node_ra_map[ra.id] = node.name

        for rs in scenario.resourcescenarios:
            #Check the attribute map created above to see if it's the right attribute.
            if attribute_id_name_map[rs.resourceattr.attr_id].lower() == attribute_name.lower():
                if rs.dataset.value is None:
                    raise Exception("Unable to view value for dataset {0}".format(rs.dataset.name))
                datasets_to_plot[node_ra_map.get(rs.resourceattr.id, rs.resourceattr.id)] = rs.dataset.value
                
    except Exception as e:
        print("An error occurred retrieving scenario {0}. Reason: {1}".format( scenario_id, e ))
        return
   
    df = {}
    for name, d in datasets_to_plot.items():
        df[name] = pd.read_json(d).iloc[:,0]

    df = pd.concat(df, axis=1)    
    df.plot()

    plt.show()


if __name__ == '__main__':
    plot_results()
