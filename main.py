import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import findnearest
from datadefination import VersionData
import os
import fitz  # pip install PyMuPDF


def split_df(input_df, split_str, key):
     input_df_lane_data = input_df.filter(regex=split_str)
     input_df_lane_position = input_df_lane_data[key]
     return input_df_lane_position


EQ_field_lane_type = ["field.left_neigbour_lane_.",
"field.left_host_lane_.", "field.right_host_lane_.",
                       "field.right_neigbour_lane_."]

EQ_field_lane_attribute = ['lane_color_', 'coeffA_', 'coeffB_', 'coeffC_', 'coeffD_', 'coeffA_std_', 'coeffB_std_',
                            'coeffC_std_', 'coeffD_std_', 'lane_end_', 'lane_startX_', 'lane_startY_', 'lane_type_',
                            'lane_track_status_', 'lane_id_', 'line_width_', 'lane_total_age_', 'lane_init_age_',
                            'lane_measure_age_', 'lane_predict_age_']

version_field_lane_type = ["field.left_neighbor_lane_.", "field.left_host_individual_.",
                            "field.right_host_individual_.", "field.right_neighbor_lane_."]

version_field_lane_attribute = ['color_', 'curve_0.zero_order_coeff_', 'curve_0.first_order_coeff_',
                                 'curve_0.second_order_coeff_', 'curve_0.third_order_coeff_',
                                 'curve_0.zero_order_coeff__var_', 'curve_0.first_order_coeff_var_',
                                 'curve_0.second_order_coeff_var_', 'curve_0.third_order_coeff_var_',
                                 'curve_0.long_distance_to_end_', 'curve_0.start_point_.x0_', 'curve_0.start_point_.y0_',
                                 'type_', 'track_status_', 'id_', 'width_', 'age_.total_age_',
                                 'age_.init_age_', 'age_.measure_age_', 'age_.predict_age_']

# EQ_data = pd.read_csv("EQ_data_mapping.csv")
# version_data = pd.read_csv("LaneMarkerInfo.csv")
version_data_ = pd.read_csv("/home/sczone/PycharmProjects/LANE_EQ_version/LaneMarkerInfo.csv")
EQ_data_ = pd.read_csv("/home/sczone/PycharmProjects/LANE_EQ_version/EyeQ4VideoLane.csv")
version_data,EQ_data = findnearest.interAndMapping(version_data_,EQ_data_)
EQ_attr_name_list = VersionData(EQ_field_lane_type,
EQ_field_lane_attribute).generatekey(EQ_field_lane_type,
EQ_field_lane_attribute)
# print(len(version_field_lane_attribute))
version_attr_name_list = VersionData(version_field_lane_type,
version_field_lane_attribute).generatekey(
     version_field_lane_type,
     version_field_lane_attribute)

version_EM_lane_type_mapping = {}
for index, type_ in enumerate(version_field_lane_type):
     version_EM_lane_type_mapping[type_] = EQ_field_lane_type[index]

version_EM_lane_attr_mapping = {}
for index, attr in enumerate(version_field_lane_attribute):
     version_EM_lane_attr_mapping[attr] = EQ_field_lane_attribute[index]

version_EM_mapping = {}
for version_lane_type, EM_lane_type in version_EM_lane_type_mapping.items():
     for version_lane_attr, EM_lane_attr in version_EM_lane_attr_mapping.items():
         version_name = "".join((version_lane_type, version_lane_attr))
         EM_name = "".join((EM_lane_type, EM_lane_attr))
         version_EM_mapping[version_name] = EM_name

col_num = len(version_field_lane_type) * len(version_field_lane_attribute)
compare_EQ_version = pd.DataFrame(np.arange(len(version_data) *col_num).reshape(len(version_data), col_num))
compare_EQ_version_result = pd.DataFrame(np.arange(len(version_data) *col_num).reshape(len(version_data), col_num))

# for row in range(len(version_data)):
#     for attr in list(version_data):
#         # print(version_data.loc[row,attr])
#         print(attr)
#         print(version_EM_mapping.get(attr))
#         # print(EQ_data.[loc,])
#     break

for lane in range(len(version_field_lane_type)):
     # print(lane)
     for attribute in range(len(version_field_lane_attribute)):
         col = lane * len(version_field_lane_attribute) + attribute
         # print(lane,col)
         version = split_df(version_data, version_field_lane_type[lane],
version_attr_name_list[col])
         EQ = split_df(EQ_data, EQ_field_lane_type[lane],
EQ_attr_name_list[col])
         for row in range(len(version)):
             # print(version[row],EQ[row])
             if version[row] != 0 and EQ[row] == 0:
                 compare_EQ_version.loc[row, col] = "false detection"
                 compare_EQ_version_result.loc[row, col] = "false detection"
             elif version[row] == 0 and EQ[row] != 0:
                 compare_EQ_version.loc[row, col] = "miss detection"
                 compare_EQ_version_result.loc[row, col] = "miss detection"
             elif version[row] == 0 and EQ[row] == 0:
                 compare_EQ_version.loc[row, col] = 0
                 compare_EQ_version_result.loc[row, col] = "correct detection"
             else:
                 compare_EQ_version.loc[row, col] = abs((EQ[row] - version[row]) / EQ[row])
                 compare_EQ_version_result.loc[row, col] = "error detection"

compare_EQ_version.columns = version_attr_name_list
compare_EQ_version.to_csv('/home/sczone/PycharmProjects/LANE_EQ_version/compare_EQ_version.csv', sep=',')
# print(compare_EQ_version)

compare_EQ_version_result.columns = compare_EQ_version.columns
compare_EQ_version_result.to_csv('/home/sczone/PycharmProjects/LANE_EQ_version/compare_EQ_version_result.csv', sep=',')
# print(compare_EQ_version_result)

# plot
sub = ['color_',
        ['curve_0.zero_order_coeff_', 'curve_0.first_order_coeff_',
         'curve_0.second_order_coeff_', 'curve_0.third_order_coeff_'],
        ['curve_0.zero_order_coeff__var_', 'curve_0.first_order_coeff_var_',
         'curve_0.second_order_coeff_var_', 'curve_0.third_order_coeff_var_'],
        ['curve_0.long_distance_to_end_', 'curve_0.start_point_.x0_', 'curve_0.start_point_.y0_'],
        ['type_', 'track_status_', 'id_', 'width_', 'age_.total_age_'],
        ['age_.init_age_', 'age_.measure_age_', 'age_.predict_age_']]
fig_title = ["color", "coeff", "coeff_var", "length", "type", "age"]
for lane_type in version_field_lane_type:
     x1 = EQ_data["field.header.stamp"]
     x2 = version_data["field.header.stamp"]
     for attr_index, attr in enumerate(sub):

         if isinstance(attr, list):

             f, ax = plt.subplots(len(attr), 1, figsize=(10, 20))

             for index, attr_ in enumerate(attr):
                 # fig, ax = plt.subplots(index + 1, 1)

                 version_lane_type_attr = "".join((lane_type, attr_))
                 EQ_lane_type_attr =
version_EM_mapping[version_lane_type_attr]

                 s1 = ax[index].plot(x1, EQ_data[EQ_lane_type_attr],
color='red', label='EQ')
                 s2 = ax[index].plot(x2,
version_data[version_lane_type_attr], color='blue', label='version')
                 # plt.suptitle(attr_)
                 plt.legend()
                 ax[index].set_title(attr_)
             fig_name = "".join((lane_type, fig_title[attr_index]))
             print(attr_index)
             f.suptitle(fig_name)
             plt.savefig(fig_name + '.jpg')
             plt.close()



         else:
             version_lane_type_attr = "".join((lane_type, attr))
             EQ_lane_type_attr = version_EM_mapping[version_lane_type_attr]
             plt.plot(x1, EQ_data[EQ_lane_type_attr], color='red',
label='EQ')
             plt.plot(x2, version_data[version_lane_type_attr],
color='blue', label='version')
             plt.legend()
             print("else", attr_index)
             plt.suptitle("".join((lane_type, fig_title[attr_index])))
             plt.savefig("".join((lane_type, fig_title[attr_index])) +
'.jpg')
             plt.close()

path = "/home/sczone/PycharmProjects/LANE_EQ_version"
dirs = os.listdir(path)
doc = fitz.open()
for i in dirs:
     if os.path.splitext(i)[1] == ".jpg":
         img_file = path+"/"+i
         imgdoc = fitz.open(img_file)
         pdfbytes = imgdoc.convert_to_pdf()
         pdf_name = i+".pdf"
         imgpdf = fitz.open(pdf_name,pdfbytes)
         doc.insert_pdf(imgpdf)
doc.save("repo.pdf")
doc.close()
