# A worked example running the pywr model through Hydra Platform 
This is a step-by-step set of instructions for running a simple water resources
 simulation model through Hydra Platform. This uses the 'Hydra-Pywr App'. This app is a software package which, amongts other things, retrieves a network from Hydra Platform, converts it into a Pywr input file, runs the pywr model, and uploads the results back to Hydra Platform. 

This app requires Hydra Platform to have the Pywr template installed. The template can be added to Hydra Platform using its 'template register' functionality. A template describes to Hydra Platform the types of nodes and links used by the model, and their attributes.

## Disclaimer
This example is broken into multiple scripts for illustration, and does not necessarily reflect how a cliient interaction should be performed.

For example, a single connection would normally be used for all communiucation with Hydra Platform. 

The code is kept as short as possible for clarity, so there is a minimum of error
checking in place! 

#Prerequisites

These examples assume a unix-based shell environment. Windows users should be able
to use powershell or other.

1. You have Python 3.6 installed

# Step 1
Get Hydra and some dependencies. This example uses 'pipenv' to install dependecnies
instead of using 'pip'. This allows us to use avoid intruding on your computer's local python installation.

```bash
    >>> pip install pipenv
    
    #Download all the correct dependencies from the Pipfile.
    #These contain hydra, pywr and the pywr app..

    #This ensures pywr builds with fewer dependencies.
    >>> export PYWR_BUILD_GLPK=true
    
    >>> pipenv install
    
    #Enter the virtual environment

    >>> pipenv shell
```

# Step 2
Create a project in Hydra. This will output a project ID to the terminal.
When prompted, the default username is 'root' and the password is empty (just hit return).

```bash
    >>> python create_project.py --name="My New Project"
    Project My New Project created with ID <project_id>
```

# Step 3
In order to import a Pywr model to Hydra first a template must be registered with Hydra. The Pywr-Hydra application includes functionality to register a template.

```bash
    >>> hydra-pywr template register
```

# Step 4
Using the pywr app, upload the network to Hydra. Choose one of the models to run. This uses the simplest one, 'simple1.json'

```bash
    >>> hydra-pywr import ../models/simple1/simple1.json <project_id>
    Network <network_id> created 

    >>> python get_network_details.py --network-id=<network_id>
    Name: 'Water Allocation Demo', 'ID': <network_id> 'Scenario ID': <scenario_id>     
```

# Step 5
Run the model

```bash
    >>> hydra-pywr run  --network-id=<network_id> --scenario-id=<scenario_id>
```

# Step 6
Create a second user to test the sharing and security features

```bash
    >>> python create_user.py --username='user2' --password='secureME' 
    User <user_id> created
```

# Step 7
Share the network with user 2, keeping 'costs' hidden.

```bash
    >>> python share_network.py --network-id=<network_id> --recipient-username='user2' --hidden-attribute='cost'
```

# Step 8
Posing as the shared user, inspect results (in this case, simulated_volume) with a simple graph. Enter your login details as prompted. A timeseries should appear. If you're using the simple model, they will all have the same value, resulting in a horizontal line.

```bash
    >>> python plot_results.py --scenario-id=<scenario_id> --attribute-name=simulated_flow
```
# Step 9
Posing as the shared user, try to access the cost values. Notice that an error occurs, as user2 does
not have permission to view the value of the cost. *This means that user 2 will be unable to run the model, as the cost value will not be exported.*

```bash
    >>> python plot_results.py --scenario-id=<scenario_id> --attribute-name=cost
    >>> An error occurred retrieving scenario 48. Reason: Unable to view value for dataset cost
```
