import csv

jpkg = 1.6 * (10 ** -13)
def add_all(data) -> float:
    summed = 0.0
    for i in range(len(data)):
        summed += data[i]
    return summed

def init_dict(dict, names):
    for i in range(len(names)):
        dict[names[i]] = 0.0

#datasheet needed for data classification and calculation.
organ_name_male = [
    'logicalBrain', 'logicalHead', 'logicalHeart', 'logicalLeftAdrenal', 'logicalLeftArmBone', 'logicalLeftBreast',
    'logicalLeftClavicle', 'logicalLeftKidney', 'logicalLeftLeg', 
    'logicalLeftLegBone', 'logicalLeftLung', 'logicalLeftOvary', 'logicalLeftScapula', 
    'logicalLeftTeste', 'logicalLowerLargeIntestine', 'logicalMaleGenitalia', 
    'logicalMiddleLowerSpine', 'logicalPancreas', 'logicalPelvis', 'logicalRibCage', 
    'logicalRightAdrenal', 'logicalRightArmBone', 'logicalRightBreast', 'logicalRightClavicle', 'logicalRightKidney', 
    'logicalRightLeg', 'logicalRightLegBone', 'logicalRightLung', 'logicalRightOvary', 
    'logicalRightScapula', 'logicalRightTeste', 'logicalSkull', 'logicalSmallIntestine', 
    'logicalSpleen', 'logicalStomach', 'logicalThymus', 'logicalThyroid', 'logicalTrunk', 
    'logicalUpperLargeIntestine', 'logicalUpperSpine', 'logicalUrinaryBladder', 'logicalUterus' 
    ]

weigh_factor = {
    "logicalThyroid": 0.04,
    "logicalBrain": 0.01,
    "logicalMaleGenitalia": 0.08,
    "logicalLeftOvary": 0.08,
    "logicalLeftTeste": 0.08,
    "logicalRightTeste": 0.08,
    "logicalLeftBreast": 0.12,
    "logicalRightBreast": 0.12,
    "logicalSmallIntestine": 0.12,
    "logicalSkull": 0.01,
    "logicalLeftClavicle": 0.01,
    "logicalRightClavicle": 0.01,
    "logicalScapula": 0.01,
    "logicalPelvis": 0.01,
    "logicalUterus": 0.08,
    "logicalStomach": 0.12,
    "logicalLeftLung": 0.12,
    "logicalRightLung": 0.12,
    "logicalLeftArmBone": 0.01,
    "logicalRightArmBone": 0.01,
    "logicalLeftLegBone": 0.01,
    "logicalRightLegBone": 0.01,
    "logicalLowerSpine": 0.01,
    "logicalUpperSpine": 0.01,
    "logicalUrinaryBladder": 0.04,
    "logicalRibCage": 0.01,
    "logicalRightLeg": 0.01,
    "logicalLeftLeg": 0.01,
    "others": 0.12
}
parname = {
    "photon": 1,
    "electron": 1,
    "muon": 1,
    "neutron_10ku": 5,
    "neutron_10kto100k": 10,
    "neutron_100to2m": 20,
    "neutron_2mto20m": 10,
    "neutron_20mp": 5,
    "proton": 5,
    "alpha": 20
}
name = input("Input the name of the file(파일 이름 입력): ")
parweigh_factor = float(input("Input the radiation weighting factor(방사선 가중계수 입력): "))

lines = []
volines = []
mass = {}
data = {}
eqdose = {}
efdose = {}
abdose = {}

init_dict(data, organ_name_male)
init_dict(mass, organ_name_male)
init_dict(eqdose, organ_name_male)
init_dict(efdose, organ_name_male)
init_dict(abdose, organ_name_male)
f = open(name)

#discern out the data that are actually needed
for line in f.readlines():
    if 'Energy Total' in line:
        lines.append(line.strip('\n'))
    elif 'Mass' in line:
        for i in range(len(organ_name_male)):
            if organ_name_male[i].strip('logical') in line:
                mass[organ_name_male[i]] = float(line.split(' ')[-2])/1000
                print(f"{organ_name_male[i]}: {mass[organ_name_male[i]]}")
    
#classify the data
for i in range(len(lines)):
    for j in range(len(organ_name_male)):
        splitted_lines = lines[i].split(' ')
        if splitted_lines[-7].strip("Run:").strip(",") == organ_name_male[j]:
            data[organ_name_male[j]] += float(splitted_lines[-1])

#calculate
for named in data.keys():
    mevtojoule = data[named] * jpkg

    if mass[named] != 0:
        abdose[named] = mevtojoule / mass[named]
    else:
        abdose[named] = 0.0
    eqdose[named] = abdose[named] * parweigh_factor
    if named in weigh_factor:
        efdose[named] = abdose[named] * weigh_factor[named]
    else:
        efdose[named] = abdose[named] * weigh_factor["others"]
    eqdose[named] = abdose[named]

fname = f"data_{name}.csv"
organ_name_male.insert(0, "organs")
dlist = ["{:.15f}".format(num) for num in data.values()]
eqlist = ["{:.15f}".format(num) for num in eqdose.values()]
eflist = ["{:.15f}".format(num) for num in efdose.values()]
ablist = ["{:.15f}".format(num) for num in abdose.values()]
dlist.insert(0, "총 증착량(energy deposition)")
eqlist.insert(0, "등가선량(equivalent dose)")
eflist.insert(0, "연간유효선량(effective dose)")
ablist.insert(0, "흡수선량(absorbed dose)")
with open(fname, "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(organ_name_male)
    writer.writerow(dlist)
    writer.writerow(eqlist)
    writer.writerow(eflist)
    writer.writerow(ablist)

print("complete")
