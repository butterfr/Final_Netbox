#!/usr/bin/env python3
import pandas, pynetbox, settings

def pullObjects(Netbox, FileInput,Column_Names):
    #Open input file and read all current csv int Ingest variable
    File = open(FileInput)
    Ingest = pandas.read_csv(File)
    File.close()
    Entries = len(Ingest)

    Current, New, duplicates = [],[],[]
    All_Objects = Netbox[0]
    ObjectNumber = len(All_Objects)
    
    #Digest all of the current csv entries
    for g in range(Entries):
        if bool('Name' in Ingest.columns) is True:
            Current.append(Ingest['Name'][g])

    #Find duplicates between the current csv entries and that of the netbox instance, then add duplicates to duplicate list
    for h in range(len(Current)):
        for i in range(ObjectNumber):
            if str(All_Objects[i]) == Current[h]:
                duplicates.append(All_Objects[i])

    #remove all items from the all_objects gathered list that are duplicates
    for j in range(len(duplicates)):
        All_Objects.remove(duplicates[j])

    ObjectNumber = len(All_Objects)

    # Combine all attributes into
    with open(FileInput, "a") as Append:
        for k in range(ObjectNumber):
            temp = Netbox[1](name=All_Objects[k])
            tempnew = []
            if 'Name' in Column_Names:
                tempnew.append(temp.name)
            if 'Slug' in Column_Names:
                tempnew.append(temp.slug)
            if 'Description' in Column_Names:
                tempnew.append(temp.description)
            if 'Color' in Column_Names:
                tempnew.append(temp.color)
            if 'VM_Role' in Column_Names:
                tempnew.append(str(temp.vm_role))
            if 'Manufacturer' in Column_Names:
                if not pandas.isna(temp.manufacturer):
                    tempnew.append(temp.manufacturer)
                else:
                    tempnew.append("")
            if 'Weight' in Column_Names:
                tempnew.append(temp.weight)
            if 'Comments' in Column_Names:
                tempnew.append(temp.comments)
            if 'Parent' in Column_Names:
                if not pandas.isna(temp.parent):
                    tempnew.append(str(temp.parent))
                else:
                    tempnew.append("")
            New = ",".join(tempnew)
            Append.write("\n" + New)

    Append.close()

def main():

    nbUrl = settings.NETBOX_URL
    nbToken = settings.NETBOX_TOKEN
    nb = pynetbox.api(nbUrl, token=nbToken)

    if settings.IGNORE_SSL_ERRORS:
        import requests
        requests.packages.urllib3.disable_warnings()
        session = requests.Session()
        session.verify = False
        nb.http_session = session


    VENDORS = settings.VENDORS
    REPO_URL = settings.REPO_URL
    SLUGS = settings.SLUGS
    REPO_BRANCH = settings.REPO_BRANCH

    # Declaration of Pynetbox API Call
    nb = pynetbox.api(nbUrl, nbToken)
    
    #Manufacturer Call
    Column_Names = ['Name','Slug','Description']
    Netbox = [nb.dcim.manufacturers.all(), nb.dcim.manufacturers.get]
    pullObjects(Netbox, "Manufacturers.csv", Column_Names)

    #Device Role Call
    Column_Names = ['Name','Slug','Description','Color','VM_Role']
    Netbox = [nb.dcim.device_roles.all(), nb.dcim.device_roles.get]
    pullObjects(Netbox, "DeviceRoles.csv", Column_Names)

    #Circuit Types Call
    Column_Names = ['Name','Slug','Description']
    Netbox = [nb.circuits.circuit_types.all(), nb.circuits.circuit_types.get]
    pullObjects(Netbox, "CircuitTypes.csv", Column_Names)  

    #Cluster Types Call
    Column_Names = ['Name','Slug','Description']
    Netbox = [nb.virtualization.cluster_types.all(), nb.virtualization.cluster_types.get]
    pullObjects(Netbox, "ClusterTypes.csv", Column_Names)

    #Platforms Call
    Column_Names = ['Name','Slug','Description','Manufacturer']
    Netbox = [nb.dcim.platforms.all(), nb.dcim.platforms.get]
    pullObjects(Netbox, "Platforms.csv", Column_Names)
    
    #Prefix_VlanRole Call
    Column_Names = ['Name','Slug','Description','Weigth']
    Netbox = [nb.ipam.roles.all(), nb.ipam.roles.get]
    pullObjects(Netbox, "Prefix_VlanRole.csv", Column_Names)

    #Providers Call  
    Column_Names = ['Name','Slug','Comments']
    Netbox = [nb.circuits.providers.all(), nb.circuits.providers.get]
    pullObjects(Netbox, "Providers.csv", Column_Names)

    #Regions Call  
    Column_Names = ['Name','Slug','Description','Parent']
    Netbox = [nb.dcim.regions.all(), nb.dcim.regions.get]
    pullObjects(Netbox, "Regions.csv", Column_Names)

if __name__ == "__main__":
    main()
