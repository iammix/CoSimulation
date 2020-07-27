import openseespy.opensees as ops
import matplotlib.pyplot as plt


number_of_elements = 10
number_of_nodes = number_of_elements + 1
izz = 1
E = 29e6
mass_per_length = 20
section_area = 10
length = 100
u = 0
analysis_duration = 0.0
step_size = 0.05
force = 100
nsteps = 1000
start_time = 0
next_node_id = 0
load_position = 0
velocity = 1

ops.wipe()
ops.wipeAnalysis()
ops.model('basic', '-ndm', 2, '-ndf', 3)

element_length = length / number_of_elements
temp = 0
for i in range(number_of_nodes):
    ops.node(i, temp, 0.0)
    temp += element_length
ops.fix(0, 1, 1, 0)
ops.fix(number_of_nodes - 1, 0, 1, 1)
ops.geomTransf('Linear', 1, 0, 0, 1)

for i in range(number_of_nodes - 1):
    ops.element('elasticBeamColumn', i, i, i + 1, section_area, E, izz, 1, '-mass',
                mass_per_length)

start_time = ops.getTime() - step_size

for i in range(nsteps + 1):
    ops.timeSeries('Path', i, '-values', 0, 1, 0, '-time', start_time,
                   start_time + 2 * step_size, 4 * step_size, '-prependZero')
    ops.pattern('Plain', i, i)
    load_position = velocity * (ops.getTime() + i * step_size)
    for j in range(number_of_nodes):
        if ops.nodeCoord(j, 1) > load_position:
            next_node_id = j
            break
    ops.eleLoad('-ele', next_node_id - 1, '-type', '-beamPoint', force,
                (load_position - ops.nodeCoord(next_node_id - 1, 1)) / (
                            ops.nodeCoord(next_node_id, 1) - ops.nodeCoord(next_node_id - 1, 1)))
    start_time += step_size

ops.constraints('Penalty', 1e+10, 1e+10)
ops.system('ProfileSPD')
ops.numberer('Plain')

ops.integrator('HHT', 0.67)
ops.algorithm('Linear')
ops.test('NormDispIncr', 1e-5, 100, 2)
ops.analysis('Transient')
current_time = 0.0
analysis_duration = nsteps * step_size
analysis_tag = 0

time = []
disp = []
while analysis_tag == 0 and current_time < analysis_duration:
    analysis_tag = ops.analyze(1, step_size)
    current_time = ops.getTime()
    time.append(current_time)
    disp.append(ops.nodeDisp(5, 2))

plt.plot(time, disp)
plt.show()

