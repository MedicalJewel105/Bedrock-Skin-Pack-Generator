import os
import json
import zipfile
import uuid
import shutil


workspace_path = os.getcwd() + '/'
temp_path = workspace_path + 'temp/'
try:
    shutil.rmtree(workspace_path+'output/')
    shutil.rmtree(temp_path)
except:
    pass
os.mkdir(temp_path)
os.mkdir(workspace_path+'output/')


print('Welcome to skin pack generator!')

with open(workspace_path+'data/skins.json', 'r') as sample_skins_json_file:
    skins_json = json.load(sample_skins_json_file)

skins = []
skins_to_translate = []

for file_name in os.listdir(workspace_path+'input'):
    # Get data for each skin
    skin_data = {}
    if file_name.endswith('.png') and file_name[:file_name.find('_')].isnumeric():
        shutil.copy(workspace_path+'input/'+file_name, temp_path+file_name)
        skin_data['geometry'] = 'geometry.humanoid.custom'
        skin_data['texture'] = file_name
        skin_data['type'] = 'free'
        if file_name.endswith('_slim.png'):
            skin_data['geometry'] += 'Slim'
            skin_data['localization_name'] = file_name[:-4][file_name.find('_')+1:]
            print(skin_data['localization_name'])
        else:
            skin_data['localization_name'] = file_name[:-4][file_name.find('_')+1:]
        skins_to_translate.append(skin_data['localization_name'])
        skin_name = file_name.replace('.png', '')[file_name.find('_')+1:file_name.rfind('_slim')]
        skin_data['order'] = int(file_name[:file_name.find('_')])
        skins.append(skin_data)
    else:
        print('Your skin name must be in format of:\n<skin_order>_<skin_name>_slim.png for alex geometry,\n<skin_order>_<skin_name>.png for steve geometry.')
        exit()

sorted_skins = sorted(skins, key=lambda skin: skin['order'])
for skin_index in range(len(sorted_skins)):
    sorted_skins[skin_index].pop('order')

skins_json['skins'] = sorted_skins

pack_localization_name = input(
    'Enter pack namespace. Note: always use different namespaces.\n')
skin_pack_name = input('Enter skin pack name. \n')
if '§' in skin_pack_name and not skin_pack_name.endswith('§r'):
    skin_pack_name += '§r'

skins_json['localization_name'] = pack_localization_name

with open(temp_path+'skins.json', 'w') as pack_skins_file:
    json.dump(skins_json, pack_skins_file, indent=4)


with open(workspace_path+'data/manifest.json', 'r') as sample_manifest_file:
    pack_manifest = json.load(sample_manifest_file)

pack_manifest['header']['name'] = skin_pack_name
pack_manifest['header']['uuid'] = str(uuid.uuid4())
pack_manifest['modules'][0]['uuid'] = str(uuid.uuid4())

with open(temp_path+'manifest.json', 'w') as pack_manifest_file:
    json.dump(pack_manifest, pack_manifest_file, indent=4)


os.mkdir(temp_path+'texts/')

translations_file = open(temp_path+'texts/en_US.lang', 'w', encoding='UTF-8')

translations_file.write(f'skinpack.{pack_localization_name}={skin_pack_name}\n')
for translating_skin in skins_to_translate:
    skin_translation_key = input(f'Name of {translating_skin}: ')
    translations_file.write(f'skin.{pack_localization_name}.{translating_skin}={skin_translation_key}\n')
translations_file.close()

zipped_skin_pack = zipfile.ZipFile(f'output/{skin_pack_name}.mcpack', mode='w')

os.chdir(temp_path)

for skin_pack_file in os.listdir(temp_path):
    if skin_pack_file == 'texts':
        zipped_skin_pack.write(skin_pack_file+'/'+os.listdir(temp_path+'texts/')[0])
    zipped_skin_pack.write(skin_pack_file)
zipped_skin_pack.close()

os.chdir(workspace_path)

shutil.rmtree(temp_path)

print('Done!')
print('Thank you for using skin pack generator. Created by MJ105#0448, GitHub link:\nhttps://github.com/MedicalJewel105/bedrock-skin-pack-generator')
