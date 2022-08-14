#!/usr/bin/env python3
from git import Repo, exc, RemoteProgress
from collections import Counter
from datetime import datetime
import yaml
import pynetbox
import glob
import argparse
import os
import settings
import sys
import re


counter = Counter(added=0, updated=0, manufacturer=0)


def update_package(path: str, branch: str):
    try:
        repo = Repo(path)
        if repo.remotes.origin.url.endswith('.git'):
            repo.remotes.origin.pull()
            repo.git.checkout(branch)
            print(f"Pulled Repo {repo.remotes.origin.url}")
    except exc.InvalidGitRepositoryError:
        pass


def slugFormat(name):
    return re.sub('\W+','-', name.lower())

YAML_EXTENSIONS = ['yml', 'yaml']

def getFiles(vendors=None):
    
    files = []
    discoveredVendors = []
    base_path = './repo/module-types/'
    if vendors:
        for r, d, f in os.walk(base_path):
            for folder in d:
                for vendor in vendors:
                    if vendor.lower() == folder.lower():
                        discoveredVendors.append({'name': folder,
                                                  'slug': slugFormat(folder)})
                        for extension in YAML_EXTENSIONS:
                            files.extend(glob.glob(base_path + folder + f'/*.{extension}'))
    else:
        for r, d, f in os.walk(base_path):
            for folder in d:
                if folder.lower() != "Testing":
                    discoveredVendors.append({'name': folder,
                                              'slug': slugFormat(folder)})
        for extension in YAML_EXTENSIONS:
            files.extend(glob.glob(base_path + f'[!Testing]*/*.{extension}'))
    return files, discoveredVendors


def readYAMl(files, **kwargs):
    slugs = kwargs.get('slugs', None)
    moduleTypes = []
    manufacturers = []
    for file in files:
        with open(file, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                continue
            manufacturer = data['manufacturer']
            data['manufacturer'] = {}
            data['manufacturer']['name'] = manufacturer
            data['manufacturer']['slug'] = slugFormat(manufacturer)

        if slugs and data['slug'] not in slugs:
            print(f"Skipping {data['model']}")
            continue

        moduleTypes.append(data)
        manufacturers.append(manufacturer)
    return moduleTypes


def createManufacturers(vendors, nb):
    all_manufacturers = {str(item): item for item in nb.dcim.manufacturers.all()}
    need_manufacturers = []
    for vendor in vendors:
        try:
            manGet = all_manufacturers[vendor["name"]]
            print(f'Manufacturer Exists: {manGet.name} - {manGet.id}')
        except KeyError:
            need_manufacturers.append(vendor)

    if not need_manufacturers:
        return

    try:
        manSuccess = nb.dcim.manufacturers.create(need_manufacturers)
        for man in manSuccess:
            print(f'Manufacturer Created: {man.name} - '
                  + f'{man.id}')
            counter.update({'manufacturer': 1})
    except pynetbox.RequestError as e:
        print(e.error)


def createInterfaces(interfaces, moduleType, nb):
    all_interfaces = {str(item): item for item in nb.dcim.interface_templates.filter(moduletype_id=moduleType)}
    need_interfaces = []
    for interface in interfaces:
        try:
            ifGet = all_interfaces[interface["name"]]
            print(f'Interface Template Exists: {ifGet.name} - {ifGet.type}'
                  + f' - {ifGet.module_type.id} - {ifGet.id}')
        except KeyError:
            interface['module_type'] = moduleType
            need_interfaces.append(interface)

    if not need_interfaces:
        return  

    try:
        ifSuccess = nb.dcim.interface_templates.create(need_interfaces)
        for intf in ifSuccess:
            print(f'Interface Template Created: {intf.name} - '
              + f'{intf.type} - {intf.module_type.id} - '
              + f'{intf.id}')
            counter.update({'updated': 1})
    except pynetbox.RequestError as e:
        print(e.error)  


def createConsolePorts(consoleports, moduleType, nb):
    all_consoleports = {str(item): item for item in nb.dcim.console_port_templates.filter(moduletype_id=moduleType)}
    need_consoleports = []
    for consoleport in consoleports:
        try:
            cpGet = all_consoleports[consoleport["name"]]
            print(f'Console Port Template Exists: {cpGet.name} - '
                  + f'{cpGet.type} - {cpGet.module_type.id} - {cpGet.id}')
        except KeyError:
            consoleport['module_type'] = moduleType
            need_consoleports.append(consoleport)

    if not need_consoleports:
        return
                
    try:
        cpSuccess = nb.dcim.console_port_templates.create(need_consoleports)
        for port in cpSuccess:
            print(f'Console Port Created: {port.name} - '
                  + f'{port.type} - {port.module_type.id} - '
                  + f'{port.id}')
            counter.update({'updated': 1})
    except pynetbox.RequestError as e:
        print(e.error)


def createPowerPorts(powerports, moduleType, nb):
    all_power_ports = {str(item): item for item in nb.dcim.power_port_templates.filter(moduletype_id=moduleType)}
    need_power_ports = []
    for powerport in powerports:
        try:
            ppGet = all_power_ports[powerport["name"]]
            print(f'Power Port Template Exists: {ppGet.name} - '
                  + f'{ppGet.type} - {ppGet.module_type.id} - {ppGet.id}')            
        except KeyError:
            powerport['module_type'] = moduleType
            need_power_ports.append(powerport)

    if not need_power_ports:
        return

    try:
        ppSuccess = nb.dcim.power_port_templates.create(need_power_ports)
        for pp in ppSuccess:
            print(f'Interface Template Created: {pp.name} - '
              + f'{pp.type} - {pp.module_type.id} - '
              + f'{pp.id}')
            counter.update({'updated': 1})
    except pynetbox.RequestError as e:
        print(e.error)

#might not need, check after successful deployment
def createConsoleServerPorts(consoleserverports, moduleType, nb):
    all_consoleserverports = {str(item): item for item in nb.dcim.console_server_port_templates.filter(moduletype_id=moduleType)}
    need_consoleserverports = []
    for csport in consoleserverports:
        try:
            cspGet = all_consoleserverports[csport["name"]]
            print(f'Console Server Port Template Exists: {cspGet.name} - '
                  + f'{cspGet.type} - {cspGet.module_type.id} - '
                  + f'{cspGet.id}')
        except KeyError:
            csport['module_type'] = moduleType
            need_consoleserverports.append(csport)

    if not need_consoleserverports:
        return

    try:
        cspSuccess = nb.dcim.console_server_port_templates.create(
            need_consoleserverports)
        for csp in cspSuccess:
            print(f'Console Server Port Created: {csp.name} - '
                  + f'{csp.type} - {csp.module_type.id} - '
                  + f'{csp.id}')
            counter.update({'updated': 1})
    except pynetbox.RequestError as e:
        print(e.error)


def createFrontPorts(frontports, moduleType, nb):
    all_frontports = {str(item): item for item in nb.dcim.front_port_templates.filter(moduletype_id=moduleType)}
    need_frontports = []
    for frontport in frontports:
        try:
            fpGet = all_frontports[frontport["name"]]
            print(f'Front Port Template Exists: {fpGet.name} - '
                  + f'{fpGet.type} - {fpGet.module_type.id} - {fpGet.id}')
        except KeyError:
            frontport['module_type'] = moduleType
            need_frontports.append(frontport)

    if not need_frontports:
        return

    all_rearports = {str(item): item for item in nb.dcim.rear_port_templates.filter(moduletype_id=moduleType)}
    for port in need_frontports:
        try:
            rpGet = all_rearports[port["rear_port"]]
            port['rear_port'] = rpGet.id
        except KeyError:
            print(f'Could not find Rear Port for Front Port: {port["name"]} - '
                  + f'{port["type"]} - {moduleType}')

    try:
        fpSuccess = nb.dcim.front_port_templates.create(need_frontports)
        for fp in fpSuccess:
            print(f'Front Port Created: {fp.name} - '
                  + f'{fp.type} - {fp.module_type.id} - '
                  + f'{fp.id}')
            counter.update({'updated': 1})
    except pynetbox.RequestError as e:
        print(e.error)


def createRearPorts(rearports, moduleType, nb):
    all_rearports = {str(item): item for item in nb.dcim.rear_port_templates.filter(moduletype_id=moduleType)}
    need_rearports = []
    for rearport in rearports:
        try:
            rpGet = all_rearports[rearport["name"]]
            print(f'Rear Port Template Exists: {rpGet.name} - {rpGet.type}'
                  + f' - {rpGet.module_type.id} - {rpGet.id}')
        except KeyError:
            rearport['module_type'] = moduleType
            need_rearports.append(rearport)

    if not need_rearports:
        return

    try:
        rpSuccess = nb.dcim.rear_port_templates.create(
            need_rearports)
        for rp in rpSuccess:
            print(f'Rear Port Created: {rp.name} - {rp.type}'
                  + f' - {rp.module_type.id} - {rp.id}')
            counter.update({'updated': 1})
    except pynetbox.RequestError as e:
        print(e.error)


def createModuleTypes(moduleTypes, nb):
    all_module_types = {str(item): item for item in nb.dcim.module_types.all()}
    #might not need this validation
    #------------------------------
    for moduleType in moduleTypes:
        try:
            mt = all_module_types[moduleType["model"]]
            print(f'Module Type Exists: {mt.manufacturer.name} - '
                  + f'{mt.model} - {mt.id}')
        except KeyError:
            try:
                mt = nb.dcim.module_types.create(moduleType)
                counter.update({'added': 1})
                print(f'Module Type Created: {mt.manufacturer.name} - '
                      + f'{mt.model} - {mt.id}')
            except pynetbox.RequestError as e:
                print(e.error)
    #------------------------------

        if "interfaces" in moduleType:
            createInterfaces(moduleType["interfaces"], mt.id, nb)

        if "power-ports" in moduleType:
            createPowerPorts(moduleType["power-ports"], mt.id, nb)

        if "power-port" in moduleType:
            createPowerPorts(moduleType["power-port"], mt.id, nb)

        if "console-ports" in moduleType:
            createConsolePorts(moduleType["console-ports"],  mt.id, nb)

        if "console-server-ports" in moduleType:
            createConsoleServerPorts(moduleType["console-server-ports"], mt.id, nb)

        if "rear-ports" in moduleType:
            createRearPorts(moduleType["rear-ports"], mt.id, nb)

        if "front-ports" in moduleType:
            createFrontPorts(moduleType["front-ports"], mt.id, nb)


def main():

    cwd = os.getcwd()
    startTime = datetime.now()

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

    parser = argparse.ArgumentParser(description='Import Netbox Module Types')
    parser.add_argument('--vendors', nargs='+', default=VENDORS,
                        help="List of vendors to import eg. apc cisco")
    parser.add_argument('--url', '--git', default=REPO_URL,
                        help="Git URL with valid Module Type YAML files")
    parser.add_argument('--slugs', nargs='+', default=SLUGS,
                        help="List of module-type slugs to import eg. ap4431 ws-c3850-24t-l")
    parser.add_argument('--branch', default=REPO_BRANCH,
                        help="Git branch to use from repo")
    args = parser.parse_args()

    try:
        if os.path.isdir('./repo'):
            print(f"Package devicetype-library is already installed, "
                  + f"updating {os.path.join(cwd, 'repo')}")
            update_package('./repo', branch=args.branch)
        else:
            repo = Repo.clone_from(args.url, os.path.join(cwd, 'repo'), branch=args.branch)
            print(f"Package Installed {repo.remotes.origin.url}")
    except exc.GitCommandError as error:
        print("Couldn't clone {} ({})".format(args.url, error))

    if not args.vendors:
        print("No Vendors Specified, Gathering All Device-Types")
        files, vendors = getFiles()
    else:
        print("Vendor Specified, Gathering All Matching Device-Types")
        files, vendors = getFiles(args.vendors)


    print(str(len(vendors)) + " Vendors Found")
    moduleTypes = readYAMl(files, slugs=args.slugs)
    print(str(len(moduleTypes)) + " Module-Types Found")
    createManufacturers(vendors, nb)
    createModuleTypes(moduleTypes, nb)

    print('---')
    print('Script took {} to run'.format(datetime.now() - startTime))
    print('{} Modules created'.format(counter['added']))
    print('{} interfaces/ports updated'.format(counter['updated']))
    print('{} manufacturers created'.format(counter['manufacturer']))


if __name__ == "__main__":
    main()
