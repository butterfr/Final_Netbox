#!/usr/bin/env python3
import pynetbox
import settings
import pandas

def digestcsv(ImportFile):
    File = open(ImportFile)
    Ingest = pandas.read_csv(File, delimiter=',')

    return Ingest

def createManufacturers(nb):
    Ingest = digestcsv("Manufacturers.csv")
    Name, Slug, Description = [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])

    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])

        #If required fields do not match any currently, then create the manufacturer with all of the ingested attributes
        if not nb.dcim.manufacturers.get(name=Name[j]) and not nb.dcim.manufacturers.get(slug=Slug[j]):
            nb.dcim.manufacturers.create(name=Name[j], slug=Slug[j], description=Description[j])
        
        #If the required fields do match any currently, replace them with the desired manufacturer ingest attributes
        elif  nb.dcim.manufacturers.get(name=Name[j]):
            Entry = nb.dcim.manufacturers.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.save()
        elif nb.dcim.manufacturers.get(slug=Slug[j]):
            Entry = nb.dcim.manufacturers.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.save()

def createCircuitTypes(nb):
    Ingest = digestcsv("CircuitTypes.csv")
    Name, Slug, Description = [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])

    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])

        #If required fields do not match any currently, then create the Circuit Types with all of the ingested attributes
        if not nb.circuits.circuit_types.get(name=Name[j]) and not nb.circuits.circuit_types.get(slug=Slug[j]):
            nb.circuits.circuit_types.create(name=Name[j], slug=Slug[j], description=Description[j])
        
        #If the required fields do match any currently, replace them with the desired Circuit Type ingest attributes
        elif  nb.circuits.circuit_types.get(name=Name[j]):
            Entry = nb.circuits.circuit_types.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.save()
        elif nb.circuits.circuit_types.get(slug=Slug[j]):
            Entry = nb.circuits.circuit_types.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.save()

def createClusterTypes(nb):
    Ingest = digestcsv("ClusterTypes.csv")
    Name, Slug, Description = [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])

    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])

        #If required fields do not match any currently, then create the Cluster Types with all of the ingested attributes
        if not nb.virtualization.cluster_types.get(name=Name[j]) and not nb.virtualization.cluster_types.get(slug=Slug[j]):
            nb.virtualization.cluster_types.create(name=Name[j], slug=Slug[j], description=Description[j])
        

        #If the required fields do match any currently, replace them with the desired Cluster Type ingest attributes
        elif  nb.virtualization.cluster_types.get(name=Name[j]):
            Entry = nb.virtualization.cluster_types.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.save()
        elif nb.virtualization.cluster_types.get(slug=Slug[j]):
            Entry = nb.virtualization.cluster_types.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.save()

def createDeviceRoles(nb):
    Ingest = digestcsv("DeviceRoles.csv")
    Name, Slug, Description, Color, vm_role = [], [], [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])
        Color.append(Ingest['Color'][i])
        vm_role.append(Ingest['VM_Role'][i])

    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])
        Color[j] = str(Color[j])
        vm_role[j] = bool(vm_role[j])

        #If required fields do not match any currently, then create the Device Roles with all of the ingested attributes
        if not nb.dcim.device_roles.get(name=Name[j]) and not nb.dcim.device_roles.get(slug=Slug[j]) and not nb.dcim.device_roles.get(color=Color[j]):
            nb.dcim.device_roles.create(name=Name[j], slug=Slug[j], description=Description[j], color=Color[j], vm_role=vm_role[j])
        
        #If the required fields do match any currently, replace them with the desired Device Roles ingest attributes
        elif  nb.dcim.device_roles.get(name=Name[j]):
            Entry = nb.dcim.device_roles.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.color=Color[j]
            Entry.vm_role=vm_role[j]
            Entry.save()
        elif nb.dcim.device_roles.get(slug=Slug[j]):
            Entry = nb.dcim.device_roles.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.color=Color[j]
            Entry.vm_role=vm_role[j]
            Entry.save()
        elif nb.dcim.device_roles.get(color=Color[j]):
            Entry = nb.dcim.device_roles.get(color=Color[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.color=Color[j]
            Entry.vm_role=vm_role[j]
            Entry.save()

def createPlatforms(nb):
    Ingest = digestcsv("Platforms.csv")
    Name, Slug, Description, Manufacturer = [], [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])
        Manufacturer.append(Ingest['Manufacturer'][i])


    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])
        Manufacturer[j] = nb.dcim.manufacturers.get(name=Manufacturer[j])

        #If required fields do not match any currently, then create the Platforms with all of the ingested attributes
        if not nb.dcim.platforms.get(name=Name[j]) and not nb.dcim.platforms.get(slug=Slug[j]):
            nb.dcim.platforms.create(name=Name[j], slug=Slug[j], description=Description[j], manufacturer=Manufacturer[j].id)
        
        #If the required fields do match any currently, replace them with the desired Platforms ingest attributes
        elif  nb.dcim.platforms.get(name=Name[j]):
            Entry = nb.dcim.platforms.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.manufacturer=Manufacturer[j].id
            Entry.save()
        elif nb.dcim.platforms.get(slug=Slug[j]):
            Entry = nb.dcim.platforms.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.manufacturer=Manufacturer[j].id
            Entry.save()

def createPrefix_VlanRole(nb):
    Ingest = digestcsv("Prefix_VlanRole.csv")
    Name, Slug, Description, Weight = [], [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])
        Weight.append(Ingest['Weight'][i])


    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])
        Weight[j] = str(Weight[j])

        #If required fields do not match any currently, then create the Prefix/Vlan Role with all of the ingested attributes
        if not nb.ipam.roles.get(name=Name[j]) and not nb.ipam.roles.get(slug=Slug[j]):
            nb.ipam.roles.create(name=Name[j], slug=Slug[j], description=Description[j], weight=Weight[j])
        
        #If the required fields do match any currently, replace them with the desired Prefix/Vlan Role ingest attributes
        elif  nb.ipam.roles.get(name=Name[j]):
            Entry = nb.ipam.roles.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.weight=Weight[j]
            Entry.save()
        elif nb.ipam.roles.get(slug=Slug[j]):
            Entry = nb.ipam.roles.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            Entry.weight=Weight[j]
            Entry.save()

def CreateProviders(nb):
    Ingest = digestcsv("Providers.csv")
    Name, Slug, Comments = [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Comments.append(Ingest['Comments'][i])


    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Comments[j] = str(Comments[j])

        #If required fields do not match any currently, then create the Providers with all of the ingested attributes
        if not nb.circuits.providers.get(name=Name[j]) and not  nb.circuits.providers.get(slug=Slug[j]):
             nb.circuits.providers.create(name=Name[j], slug=Slug[j], comments=Comments[j])
        
        #If the required fields do match any currently, replace them with the desired Providers ingest attributes
        elif  nb.circuits.providers.get(name=Name[j]):
            Entry = nb.circuits.providers.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.comments = Comments[j]
            Entry.save()
        elif nb.circuits.providers.get(slug=Slug[j]):
            Entry = nb.circuits.providers.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.comments = Comments[j]
            Entry.save()

def createRegions(nb):
    Ingest = digestcsv("Regions.csv")
    Name, Slug, Description, Parent = [], [], [], []
    Entries = range(len(Ingest))

    for i in Entries:
        Name.append(Ingest['Name'][i])
        Slug.append(Ingest['Slug'][i])
        Description.append(Ingest['Description'][i])
        Parent.append(Ingest['Parent'][i])

    for j in Entries:
        Name[j] = str(Name[j])
        Slug[j] = str(Slug[j])
        Description[j] = str(Description[j])
        Parent[j] = nb.dcim.regions.get(name=Parent[j])

        #If required fields do not match any currently, then create the Regions with all of the ingested attributes
        if not nb.dcim.regions.get(name=Name[j]) and not nb.dcim.regions.get(slug=Slug[j]):
            if pandas.isna(Parent[j]) is True:
                nb.dcim.regions.create(name=Name[j], slug=Slug[j], description=Description[j])
            else:
                nb.dcim.regions.create(name=Name[j], slug=Slug[j], description=Description[j], parent=Parent[j].id)
        
        #If the required fields do match any currently, replace them with the desired Region ingest attributes
        elif  nb.dcim.regions.get(name=Name[j]):
            Entry = nb.dcim.regions.get(name=Name[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            if pandas.isna(Parent[j]) is True:
                Entry.save()
            else:
                Entry.parent=Parent[j].id
                Entry.save()
        elif nb.dcim.regions.get(slug=Slug[j]):
            Entry = nb.dcim.regions.get(slug=Slug[j])
            Entry.name = Name[j]
            Entry.slug = Slug[j]
            Entry.description = Description[j]
            if pandas.isna(Parent[j]) is True:
                Entry.save()
            else:
                Entry.parent=Parent[j].id
                Entry.save()

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

    createManufacturers(nb)
    createCircuitTypes(nb)
    createClusterTypes(nb)
    createDeviceRoles(nb)
    createPlatforms(nb)
    createPrefix_VlanRole(nb)
    CreateProviders(nb)
    createRegions(nb)

if __name__ == "__main__":
    main()
