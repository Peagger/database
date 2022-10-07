

import os
insert_data={
    'Picid':'6730018',
    'local_path':'./pic/6730018.jpg',
    'master':'0',
    'delet':'0',
    'download':'0',
    'artist':'hiki_niito',
    'character':"gany'u_(genshin_impact)",
    'copyright':'genshin_impact',
    'metadata':'absurdres,highres',
    'tag':'1girl,ahoge,ass,bangs',
    'origin_url':'https://img3.gelbooru.com//samples/d3/c0/sample_d3c04b98e118908fc575fc146a44ec6b.jpg'   
}

id={'1':','.join([])}
#print(id)
a="let's go"
print(a)
a.replace('\'','\'\'')
print(a)
print(insert_data)
for i,j in insert_data.items():
    insert_data[i]=j.replace('\'','\'\'')
print(insert_data)

