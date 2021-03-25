#!/usr/bin/env python3

from optparse import OptionParser
import os

# defining the arguments that need to be passed to the script
arguments = OptionParser()
arguments.add_option('-l', '--lastz', dest='lastz', help='lastz file')
arguments.add_option('-o', '--out', dest='out', help='output name')

(options, args) = arguments.parse_args()
if not options.lastz or not options.out:
    # if one of the arguments is missing
    print('\n----------> A mandatory option is missing !\n')  # raise an error
    arguments.print_help()  # and provide the help
    exit(-1)  # exit the script

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The plotting will be done separately for the two orientations so that I don't need to account for it in the script
# Because in the extraction of windows the LINE is always kept at the 5' to 3' orientation, the LEFT side is always 5'
# and the RIGHT side is always 3'
# The thing that is different between the hits is the orientation of the satellite in relation to LINE (which will be same or different)

# here the left side is extended to 1
# therefore the RIGHT window of G is extended LEFT
# and the RIGHT side of g
def extend_left(q_start, r_start):
    if int(q_start) == 1:
        r_end = int(r_start) - 1 - 1

    else:
        missing = int(q_start) - 1
        r_end = int(r_start) - missing - 1 - 1
    return r_end

# here the right side is extended based on the length of the query
# therefore the LEFT side of G is extended RIGHT
# and the LEFT side of g is extended RIGHT
def extend_right(q_length, q_start, q_alignment, r_start, r_alignment):
    q_end = int(q_start) + int(q_alignment) - 1
    if q_end >= int(q_length):
        r_end = int(r_start) + int(r_alignment) - 1 - 1

    else:
        missing = int(q_length) - q_end
        r_end = int(r_start) + int(r_alignment) - 1 + missing - 1

    return r_end

end_3 = None
end_5 = None
number_of_3_end_hits = 0
number_of_5_end_hits = 0
number_of_hits_mapped = 0
# I will document all the insertion points for each hit
insertion_points = {}

#print(len(end_3))
with open(options.lastz) as l:
    for line in l:
        items = line.split()
        #print(items)
        if not end_3 and not end_5:
            end_3 = [0] * int(items[1])
            end_5 = [0] * int(items[1])

        # the 5' end
        if '__LEFT__' in items[5]:
            #print(items)
            if items[9] == '-' and 1 <= int(items[7]) <= 5:
                # the left side of the left end is the insertion point
                insertion_point = extend_left(int(items[7]), int(items[2]))
                #print(insertion_point)
                number_of_5_end_hits += 1
                number_of_hits_mapped += 1
                #a = '%s\t%s\n' % (items[5], str(insertion_point))
                #out_insertion_points.write(a)
                end_5[insertion_point] += 1
                if items[5].split('__')[3] not in insertion_points.keys():
                    insertion_points[items[5].split('__')[3]] = [[items[5], str(insertion_point)]]
                else:
                    insertion_points[items[5].split('__')[3]].append([items[5], str(insertion_point)])

            if items[9] == '+' and int(items[6]) - 5 <= int(items[7]) + int(items[8]) - 1 <= int(items[6]):
                # the right side of the left side is the insertion point
                insertion_point = extend_right(int(items[6]), int(items[7]), int(items[8]), int(items[2]), int(items[3]))
                #print(insertion_point)
                number_of_5_end_hits += 1
                number_of_hits_mapped += 1
                #a = '%s\t%s\n' % (items[5], str(insertion_point))
                #out_insertion_points.write(a)
                end_5[insertion_point] += 1
                if items[5].split('__')[3] not in insertion_points.keys():
                    insertion_points[items[5].split('__')[3]] = [[items[5], str(insertion_point)]]
                else:
                    insertion_points[items[5].split('__')[3]].append([items[5], str(insertion_point)])

        # the 3' end
        if '__RIGHT__' in items[5]:
            #print(items)
            if items[9] == '-' and int(items[6]) - 5 <= int(items[7]) + int(items[8]) - 1 <= int(items[6]):
                # the right side of the right end is the insertion point
                insertion_point = extend_right(int(items[6]), int(items[7]), int(items[8]), int(items[2]), int(items[3]))
                #print(insertion_point)
                number_of_3_end_hits += 1
                number_of_hits_mapped += 1
                # a = '%s\t%s\n' % (items[5], str(insertion_point))
                # out_insertion_points.write(a)
                end_3[insertion_point] += 1
                if items[5].split('__')[3] not in insertion_points.keys():
                    insertion_points[items[5].split('__')[3]] = [[items[5], str(insertion_point)]]
                else:
                    insertion_points[items[5].split('__')[3]].append([items[5], str(insertion_point)])

            if items[9] == '+' and 1 <= int(items[7]) <= 5:
                # the left side of the right end is the insertion point
                insertion_point = extend_left(int(items[7]), int(items[2]))
                #print(insertion_point)
                number_of_3_end_hits += 1
                number_of_hits_mapped += 1
                #a = '%s\t%s\n' % (items[5], str(insertion_point))
                #out_insertion_points.write(a)
                end_3[insertion_point] += 1
                if items[5].split('__')[3] not in insertion_points.keys():
                    insertion_points[items[5].split('__')[3]] = [[items[5], str(insertion_point)]]
                else:
                    insertion_points[items[5].split('__')[3]].append([items[5], str(insertion_point)])

# print(end_5)
# print(end_3)
out_end_5 = open(options.out+'__5_end', 'w')
out_end_3 = open(options.out+'__3_end', 'w')

end_5 = [str(x) for x in end_5]
end_3 = [str(x) for x in end_3]

out_end_5.write('\t'.join(end_5))
out_end_3.write('\t'.join(end_3))

out_end_5.close()
out_end_3.close()

out_paired_insertion_points = open(options.out+'__paired_insertion_points', 'w')
out_not_paired_insertion_points = open(options.out+'__not_paired_insertion_points', 'w')
for key, val in insertion_points.items():
    if len(val) == 2:
        val = [j for i in val for j in i]
        val = '\t'.join(val)
        #print(val)
        out_paired_insertion_points.write(val+'\n')
    else:
        val = [j for i in val for j in i]
        val = '\t'.join(val)
        #print(val)
        out_not_paired_insertion_points.write(val + '\n')

out_not_paired_insertion_points.close()
out_paired_insertion_points.close()

plotting_command = 'Rscript --vanilla /mnt/raid/users/tihana/tihana_rscipts/plotting_density_profile/plotting_density_profile_of_LINE_insertion.R %s %s' % (options.out+'__5_end', options.out+'__5_end.png')
os.system(plotting_command)
#print(plotting_command)
plotting_command = 'Rscript --vanilla /mnt/raid/users/tihana/tihana_rscipts/plotting_density_profile/plotting_density_profile_of_LINE_insertion.R %s %s' % (options.out+'__3_end', options.out+'__3_end.png')
os.system(plotting_command)
#print(plotting_command)

combining_command = 'convert -append %s %s %s' % (options.out+'__5_end.png', options.out+'__3_end.png', options.out+'__5_and_3_end.png')
os.system(combining_command)

a = "number of plotted 3' ends: %s" % str(number_of_3_end_hits)
print(a)
a = "number of plotted 5' ends: %s" % str(number_of_5_end_hits)
print(a)
a = "number of hits mapped: %s" % str(number_of_hits_mapped)
print(a)
#print(insertion_points)
