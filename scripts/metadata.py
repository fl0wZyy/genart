import json

dict_data = {
  "description": "First Generation of Poetry Displayed in the L'art Museum. Not yet reavealed.",
  "name":"L'art Pour L'art Gen I",
  "imageIPFS": "QmXcpzLdyRZeHuH1Jpg6E6Dc7YvUeKBYm5RpcM95dVY3c2",
  "tokenId": 0,
}

for i in range(999):
    new_dict = dict_data
    new_dict["tokenId"] = i
    with open(f'{i}', "w") as fp:
        json.dump(new_dict, fp)