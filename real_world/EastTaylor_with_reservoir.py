# SCRIPT TO RUN THE DECADAL SIMULATION USING THE NEW PFTOOLS
#intake cell at 41, 21
#release cell at 41,22



import sys
import os
from datetime import datetime
from parflow.tools import Run
from parflow.tools.fs import mkdir, cp, get_absolute_path, exists
from parflow.tools.settings import set_working_directory
import calendar

"""
This script runs parflow-clm for East Taylor - CONUS2 for one water year.
"""

RELEASE_WATER = True

#-----------------------------------------------------------------------------
#Get initial inputs
#-----------------------------------------------------------------------------
#ignore this, leave it at 1000m
resolution = 1000

#year for which to run the simulations
year_run = 2003
runname =f'EastTaylor_{year_run}'

#change path to forcing
forcing_path = f'{os.getcwd()}/reservoir_inputs/NLDAS/WY{year_run}/'

# SET THIS TO TRUE if you changed the topology or are not sure the forcing has the same topology as what you're running with
redistribute_forcing = True

#set the directory where you want to run/get outputs and where the inputs are
if RELEASE_WATER:
    directory_running = f'simulations/WY{year_run}_with_reservoir_releasing_15715'
else:
    directory_running = f'simulations/WY{year_run}_with_reservoir'
directory_inputs = f'{os.getcwd()}/reservoir_inputs/'

#set this to true if you want to start the simulations from initial conditions in 'inputs/initial_conditions_for_2003/'
restart_from_previous = True

inputs_name = f'EastTaylor_1000m'

print(directory_inputs)
#Create output directory if it doesn't exist
if os.path.exists(directory_running) == False:
    os.makedirs(directory_running)


if calendar.isleap(year_run):
    n_hours = 8784
else:
    n_hours = 8760

run = Run(runname, __file__)
run.FileVersion = 4

#-----------------------------------------------------------------------------
# Set Processor topology
#-----------------------------------------------------------------------------

run.Process.Topology.P = 4
run.Process.Topology.Q = 4
run.Process.Topology.R = 1

nproc = run.Process.Topology.P * run.Process.Topology.Q * run.Process.Topology.R

#-----------------------------------------------------------------------------
# Make a directory for the simulation and copy inputs into it
#-----------------------------------------------------------------------------

set_working_directory(directory_running)

filename_slopex = f'{inputs_name}.slopex_resampled.pfb'
filename_slopey = f'{inputs_name}.slopey_resampled.pfb'
filename_mannings = f'{inputs_name}.mannings.pfb'
#filename_pme = f'{inputs_name}.pme.pfb'
filename_indicator = f'{inputs_name}.indicator.pfb'
filename_depthtobedrock = f'{inputs_name}.depthtobedrock.pfb'
filename_solidfile = f'{inputs_name}.solidfile_resampled.pfsol'

filename_drv_vegm = 'drv_vegm.dat'
filename_drv_vegp = 'drv_vegp.dat'
filename_drv_clmin = 'drv_clmin.dat'

istep = 0

filename_drv_clmin_in = 'drv_clmin_restart.dat'

if istep > 0: #restarting!
    for i in range(0,run.Process.Topology.P*run.Process.Topology.Q):
        rst_timestamp = str(int(istep)).rjust(5, '0')
        cp(f'clm.rst.00000.{i}',f'clm.rst.{rst_timestamp}.{i}')
    t0_istep = str(int(istep)).rjust(5, '0')
    filename_initialpressure = f'{runname}.out.press.{t0_istep}.pfb'
elif restart_from_previous==True:
    filename_initialpressure = f'EastTaylor_1000m_2002.out.press.08760.pfb'
        
    cp(f'{directory_inputs}/initial_conditions_for_2003/{filename_initialpressure}')
    for i in range(0,run.Process.Topology.P*run.Process.Topology.Q):
        rst_timestamp = str(int(istep)).rjust(5, '0')
        cp(f'{directory_inputs}/initial_conditions_for_2003/clm.rst.00000.{i}')
else:
    filename_drv_clmin_in = 'drv_clmin_newstart.dat'

print(f'{directory_inputs}{filename_slopex}')
# ParFlow Inputs
cp(f'{directory_inputs}{filename_slopex}')
cp(f'{directory_inputs}{filename_slopey}')
cp(f'{directory_inputs}{filename_mannings}')
#cp(f'{directory_inputs}{filename_pme}')
cp(f'{directory_inputs}{filename_indicator}')
cp(f'{directory_inputs}{filename_depthtobedrock}')
cp(f'{directory_inputs}{filename_solidfile}')

cp(f'{directory_inputs}{filename_drv_clmin_in}',filename_drv_clmin)
cp(f'{directory_inputs}{filename_drv_vegm}')
cp(f'{directory_inputs}{filename_drv_vegp}')

#-----------------------------------------------------------------------------
# Computational Grid
#-----------------------------------------------------------------------------

run.ComputationalGrid.Lower.X = 0.0
run.ComputationalGrid.Lower.Y = 0.0
run.ComputationalGrid.Lower.Z = 0.0

run.ComputationalGrid.DX = resolution
run.ComputationalGrid.DY = resolution
run.ComputationalGrid.DZ = 200.0

run.ComputationalGrid.NX = int(68000/resolution)
run.ComputationalGrid.NY = int(52000/resolution)
run.ComputationalGrid.NZ = 10

#-----------------------------------------------------------------------------
# Names of the GeomInputs
#-----------------------------------------------------------------------------

run.GeomInput.Names = "domaininput indi_input"

#-----------------------------------------------------------------------------
# Domain Geometry Input
#-----------------------------------------------------------------------------

run.GeomInput.domaininput.InputType = 'SolidFile'
run.GeomInput.domaininput.GeomNames = 'domain'
run.GeomInput.domaininput.FileName = filename_solidfile

#-----------------------------------------------------------------------------
# Domain Geometry
#-----------------------------------------------------------------------------

run.Geom.domain.Patches = "top bottom side"

#-----------------------------------------------------------------------------
# Indicator Geometry Input
#-----------------------------------------------------------------------------

run.GeomInput.indi_input.InputType = 'IndicatorField'
run.GeomInput.indi_input.GeomNames = 's1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8 b1 b2'
run.Geom.indi_input.FileName = filename_indicator

run.GeomInput.s1.Value = 1
run.GeomInput.s2.Value = 2
run.GeomInput.s3.Value = 3
run.GeomInput.s4.Value = 4
run.GeomInput.s5.Value = 5
run.GeomInput.s6.Value = 6
run.GeomInput.s7.Value = 7
run.GeomInput.s8.Value = 8
run.GeomInput.s9.Value = 9
run.GeomInput.s10.Value = 10
run.GeomInput.s11.Value = 11
run.GeomInput.s12.Value = 12
run.GeomInput.s13.Value = 13

run.GeomInput.b1.Value = 19
run.GeomInput.b2.Value = 20

run.GeomInput.g1.Value = 21
run.GeomInput.g2.Value = 22
run.GeomInput.g3.Value = 23
run.GeomInput.g4.Value = 24
run.GeomInput.g5.Value = 25
run.GeomInput.g6.Value = 26
run.GeomInput.g7.Value = 27
run.GeomInput.g8.Value = 28

#--------------------------------------------
# variable dz assignments
#------------------------------------------
run.Solver.Nonlinear.VariableDz = True
run.dzScale.GeomNames = 'domain'
run.dzScale.Type = 'nzList'
run.dzScale.nzListNumber = 10

# 10 layers, starts at 0 for the bottom to 9 at the top
# note this is opposite Noah/WRF
# layers are 0.1 m, 0.3 m, 0.6 m, 1.0 m, 5.0 m, 10.0 m, 25.0 m, 50.0 m, 100.0m, 200.0 m
# 200 m * 1.0 = 200 m
run.Cell._0.dzScale.Value = 1.0
# 200 m * .5 = 100 m 
run.Cell._1.dzScale.Value = 0.5
# 200 m * .25 = 50 m 
run.Cell._2.dzScale.Value = 0.25
# 200 m * 0.125 = 25 m 
run.Cell._3.dzScale.Value = 0.125
# 200 m * 0.05 = 10 m 
run.Cell._4.dzScale.Value = 0.05
# 200 m * .025 = 5 m 
run.Cell._5.dzScale.Value = 0.025
# 200 m * .005 = 1 m 
run.Cell._6.dzScale.Value = 0.005
# 200 m * 0.003 = 0.6 m 
run.Cell._7.dzScale.Value = 0.003
# 200 m * 0.0015 = 0.3 m 
run.Cell._8.dzScale.Value = 0.0015
# 200 m * 0.0005 = 0.1 m = 10 cm which is default top Noah layer
run.Cell._9.dzScale.Value = 0.0005

#------------------------------------------------------------------------------
# Flow Barrier defined by Shangguan Depth to Bedrock
#--------------------------------------------------------------

run.Solver.Nonlinear.FlowBarrierZ = True
run.FBz.Type = 'PFBFile'
run.Geom.domain.FBz.FileName = filename_depthtobedrock

#-----------------------------------------------------------------------------
# Permeability (values in m/hr)
#-----------------------------------------------------------------------------

run.Geom.Perm.Names = 'domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8 b1 b2'

run.Geom.domain.Perm.Type = 'Constant'
run.Geom.domain.Perm.Value = 0.02

run.Geom.s1.Perm.Type = 'Constant'
run.Geom.s1.Perm.Value = 0.269022595

run.Geom.s2.Perm.Type = 'Constant'
run.Geom.s2.Perm.Value = 0.043630356

run.Geom.s3.Perm.Type = 'Constant'
run.Geom.s3.Perm.Value = 0.015841225

run.Geom.s4.Perm.Type = 'Constant'
run.Geom.s4.Perm.Value = 0.007582087

run.Geom.s5.Perm.Type = 'Constant'
run.Geom.s5.Perm.Value = 0.01818816

run.Geom.s6.Perm.Type = 'Constant'
run.Geom.s6.Perm.Value = 0.005009435

run.Geom.s7.Perm.Type = 'Constant'
run.Geom.s7.Perm.Value = 0.005492736

run.Geom.s8.Perm.Type = 'Constant'
run.Geom.s8.Perm.Value = 0.004675077

run.Geom.s9.Perm.Type = 'Constant'
run.Geom.s9.Perm.Value = 0.003386794

run.Geom.s10.Perm.Type = 'Constant'
run.Geom.s10.Perm.Value = 0.004783973

run.Geom.s11.Perm.Type = 'Constant'
run.Geom.s11.Perm.Value = 0.003979136

run.Geom.s12.Perm.Type = 'Constant'
run.Geom.s12.Perm.Value = 0.006162952

run.Geom.s13.Perm.Type = 'Constant'
run.Geom.s13.Perm.Value = 0.005009435

run.Geom.b1.Perm.Type = 'Constant'
run.Geom.b1.Perm.Value = 0.005

run.Geom.b2.Perm.Type = 'Constant'
run.Geom.b2.Perm.Value = 0.01

run.Geom.g1.Perm.Type = 'Constant'
run.Geom.g1.Perm.Value = 0.02

run.Geom.g2.Perm.Type = 'Constant'
run.Geom.g2.Perm.Value = 0.03

run.Geom.g3.Perm.Type = 'Constant'
run.Geom.g3.Perm.Value = 0.04

run.Geom.g4.Perm.Type = 'Constant'
run.Geom.g4.Perm.Value = 0.05

run.Geom.g5.Perm.Type = 'Constant'
run.Geom.g5.Perm.Value = 0.06

run.Geom.g6.Perm.Type = 'Constant'
run.Geom.g6.Perm.Value = 0.08

run.Geom.g7.Perm.Type = 'Constant'
run.Geom.g7.Perm.Value = 0.1

run.Geom.g8.Perm.Type = 'Constant'
run.Geom.g8.Perm.Value = 0.2

run.Perm.TensorType = 'TensorByGeom'
run.Geom.Perm.TensorByGeom.Names = 'domain b1 b2 g1 g2 g4 g5 g6 g7'

run.Geom.domain.Perm.TensorValX = 1.0
run.Geom.domain.Perm.TensorValY = 1.0
run.Geom.domain.Perm.TensorValZ = 1.0

run.Geom.b1.Perm.TensorValX = 1.0
run.Geom.b1.Perm.TensorValY = 1.0
run.Geom.b1.Perm.TensorValZ = 0.1

run.Geom.b2.Perm.TensorValX = 1.0
run.Geom.b2.Perm.TensorValY = 1.0
run.Geom.b2.Perm.TensorValZ = 0.1

run.Geom.g1.Perm.TensorValX = 1.0
run.Geom.g1.Perm.TensorValY = 1.0
run.Geom.g1.Perm.TensorValZ = 0.1

run.Geom.g2.Perm.TensorValX = 1.0
run.Geom.g2.Perm.TensorValY = 1.0
run.Geom.g2.Perm.TensorValZ = 0.1

run.Geom.g4.Perm.TensorValX = 1.0
run.Geom.g4.Perm.TensorValY = 1.0
run.Geom.g4.Perm.TensorValZ = 0.1

run.Geom.g5.Perm.TensorValX = 1.0
run.Geom.g5.Perm.TensorValY = 1.0
run.Geom.g5.Perm.TensorValZ = 0.1

run.Geom.g6.Perm.TensorValX = 1.0
run.Geom.g6.Perm.TensorValY = 1.0
run.Geom.g6.Perm.TensorValZ = 0.1

run.Geom.g7.Perm.TensorValX = 1.0
run.Geom.g7.Perm.TensorValY = 1.0
run.Geom.g7.Perm.TensorValZ = 0.1

#-----------------------------------------------------------------------------
# Specific Storage
#-----------------------------------------------------------------------------

run.SpecificStorage.Type = 'Constant'
run.SpecificStorage.GeomNames = 'domain'
run.Geom.domain.SpecificStorage.Value = 1.0e-4

#-----------------------------------------------------------------------------
# Phases
#-----------------------------------------------------------------------------

run.Phase.Names = 'water'
run.Phase.water.Density.Type = 'Constant'
run.Phase.water.Density.Value = 1.0
run.Phase.water.Viscosity.Type = 'Constant'
run.Phase.water.Viscosity.Value = 1.0

#-----------------------------------------------------------------------------
# Contaminants
#-----------------------------------------------------------------------------

run.Contaminants.Names = ''

#-----------------------------------------------------------------------------
# Gravity
#-----------------------------------------------------------------------------

run.Gravity = 1.0

#-----------------------------------------------------------------------------
# Timing (time units is set by units of permeability)
#-----------------------------------------------------------------------------

run.TimingInfo.BaseUnit = 1.0
run.TimingInfo.StartCount = istep
run.TimingInfo.StartTime = istep
# run.TimingInfo.StopTime =n_hours
run.TimingInfo.StopTime = 10
run.TimingInfo.DumpInterval = 1
run.TimeStep.Type = 'Constant'
run.TimeStep.Value = 1

# run.TimeStep.Type = 'Growth'
# run.TimeStep.InitialStep = 500
# run.TimeStep.GrowthFactor = 1.1
# run.TimeStep.MaxStep = 2000
# run.TimeStep.MinStep = 1

#-----------------------------------------------------------------------------
# Porosity
#-----------------------------------------------------------------------------

run.Geom.Porosity.GeomNames = 'domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8'

run.Geom.domain.Porosity.Type = 'Constant'
run.Geom.domain.Porosity.Value = 0.33

run.Geom.s1.Porosity.Type = 'Constant'
run.Geom.s1.Porosity.Value = 0.375

run.Geom.s2.Porosity.Type = 'Constant'
run.Geom.s2.Porosity.Value = 0.39

run.Geom.s3.Porosity.Type = 'Constant'
run.Geom.s3.Porosity.Value = 0.387

run.Geom.s4.Porosity.Type = 'Constant'
run.Geom.s4.Porosity.Value = 0.439

run.Geom.s5.Porosity.Type = 'Constant'
run.Geom.s5.Porosity.Value = 0.489

run.Geom.s6.Porosity.Type = 'Constant'
run.Geom.s6.Porosity.Value = 0.399

run.Geom.s7.Porosity.Type = 'Constant'
run.Geom.s7.Porosity.Value = 0.384

run.Geom.s8.Porosity.Type = 'Constant'
run.Geom.s8.Porosity.Value = 0.482

run.Geom.s9.Porosity.Type = 'Constant'
run.Geom.s9.Porosity.Value = 0.442

run.Geom.s10.Porosity.Type = 'Constant'
run.Geom.s10.Porosity.Value = 0.385

run.Geom.s11.Porosity.Type = 'Constant'
run.Geom.s11.Porosity.Value = 0.481

run.Geom.s12.Porosity.Type = 'Constant'
run.Geom.s12.Porosity.Value = 0.459

run.Geom.s13.Porosity.Type = 'Constant'
run.Geom.s13.Porosity.Value = 0.399

run.Geom.g1.Porosity.Type = 'Constant'
run.Geom.g1.Porosity.Value = 0.33

run.Geom.g2.Porosity.Type = 'Constant'
run.Geom.g2.Porosity.Value = 0.33

run.Geom.g3.Porosity.Type = 'Constant'
run.Geom.g3.Porosity.Value = 0.33

run.Geom.g4.Porosity.Type = 'Constant'
run.Geom.g4.Porosity.Value = 0.33

run.Geom.g5.Porosity.Type = 'Constant'
run.Geom.g5.Porosity.Value = 0.33

run.Geom.g6.Porosity.Type = 'Constant'
run.Geom.g6.Porosity.Value = 0.33

run.Geom.g7.Porosity.Type = 'Constant'
run.Geom.g7.Porosity.Value = 0.33

run.Geom.g8.Porosity.Type = 'Constant'
run.Geom.g8.Porosity.Value = 0.33

#-----------------------------------------------------------------------------
# Domain
#-----------------------------------------------------------------------------

run.Domain.GeomName = 'domain'

#----------------------------------------------------------------------------
# Mobility
#----------------------------------------------------------------------------

run.Phase.water.Mobility.Type = 'Constant'
run.Phase.water.Mobility.Value = 1.0

#-----------------------------------------------------------------------------
# Wells
#-----------------------------------------------------------------------------

run.Wells.Names = ''

#-----------------------------------------------------------------------------
# Relative Permeability
#-----------------------------------------------------------------------------

run.Phase.RelPerm.Type = 'VanGenuchten'
run.Phase.RelPerm.GeomNames = 'domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13'

run.Geom.domain.RelPerm.Alpha = 1.
run.Geom.domain.RelPerm.N = 3.0
run.Geom.domain.RelPerm.NumSamplePoints = 20000
run.Geom.domain.RelPerm.MinPressureHead = -300
run.Geom.domain.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s1.RelPerm.Alpha = 3.548
run.Geom.s1.RelPerm.N = 4.162
run.Geom.s1.RelPerm.NumSamplePoints = 20000
run.Geom.s1.RelPerm.MinPressureHead = -300
run.Geom.s1.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s2.RelPerm.Alpha = 3.467
run.Geom.s2.RelPerm.N = 2.738
run.Geom.s2.RelPerm.NumSamplePoints = 20000
run.Geom.s2.RelPerm.MinPressureHead = -300
run.Geom.s2.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s3.RelPerm.Alpha = 2.692
run.Geom.s3.RelPerm.N = 2.445
run.Geom.s3.RelPerm.NumSamplePoints = 20000
run.Geom.s3.RelPerm.MinPressureHead = -300
run.Geom.s3.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s4.RelPerm.Alpha = 0.501
run.Geom.s4.RelPerm.N = 2.659
run.Geom.s4.RelPerm.NumSamplePoints = 20000
run.Geom.s4.RelPerm.MinPressureHead = -300
run.Geom.s4.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s5.RelPerm.Alpha = 0.661
run.Geom.s5.RelPerm.N = 2.659
run.Geom.s5.RelPerm.NumSamplePoints = 20000
run.Geom.s5.RelPerm.MinPressureHead = -300
run.Geom.s5.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s6.RelPerm.Alpha = 1.122
run.Geom.s6.RelPerm.N = 2.479
run.Geom.s6.RelPerm.NumSamplePoints = 20000
run.Geom.s6.RelPerm.MinPressureHead = -300
run.Geom.s6.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s7.RelPerm.Alpha = 2.089
run.Geom.s7.RelPerm.N = 2.318
run.Geom.s7.RelPerm.NumSamplePoints = 20000
run.Geom.s7.RelPerm.MinPressureHead = -300
run.Geom.s7.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s8.RelPerm.Alpha = 0.832
run.Geom.s8.RelPerm.N = 2.514
run.Geom.s8.RelPerm.NumSamplePoints = 20000
run.Geom.s8.RelPerm.MinPressureHead = -300
run.Geom.s8.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s9.RelPerm.Alpha = 1.585
run.Geom.s9.RelPerm.N = 2.413
run.Geom.s9.RelPerm.NumSamplePoints = 20000
run.Geom.s9.RelPerm.MinPressureHead = -300
run.Geom.s9.RelPerm.InterpolationMethod = 'Linear'


run.Geom.s10.RelPerm.Alpha = 3.311
run.Geom.s10.RelPerm.N = 2.202
run.Geom.s10.RelPerm.NumSamplePoints = 20000
run.Geom.s10.RelPerm.MinPressureHead = -300
run.Geom.s10.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s11.RelPerm.Alpha = 1.622
run.Geom.s11.RelPerm.N = 2.318
run.Geom.s11.RelPerm.NumSamplePoints = 20000
run.Geom.s11.RelPerm.MinPressureHead = -300
run.Geom.s11.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s12.RelPerm.Alpha = 1.514
run.Geom.s12.RelPerm.N = 2.259
run.Geom.s12.RelPerm.NumSamplePoints = 20000
run.Geom.s12.RelPerm.MinPressureHead = -300
run.Geom.s12.RelPerm.InterpolationMethod = 'Linear'

run.Geom.s13.RelPerm.Alpha = 1.122
run.Geom.s13.RelPerm.N = 2.479
run.Geom.s13.RelPerm.NumSamplePoints = 20000
run.Geom.s13.RelPerm.MinPressureHead = -300
run.Geom.s13.RelPerm.InterpolationMethod = 'Linear'

#-----------------------------------------------------------------------------
# Saturation
#-----------------------------------------------------------------------------

run.Phase.Saturation.Type = 'VanGenuchten'
run.Phase.Saturation.GeomNames = 'domain s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13'

run.Geom.domain.Saturation.Alpha = 1.
run.Geom.domain.Saturation.N = 3.
run.Geom.domain.Saturation.SRes = 0.001
run.Geom.domain.Saturation.SSat = 1.0

run.Geom.s1.Saturation.Alpha = 3.548
run.Geom.s1.Saturation.N = 4.162
run.Geom.s1.Saturation.SRes = 0.0001
run.Geom.s1.Saturation.SSat = 1.0

run.Geom.s2.Saturation.Alpha = 3.467
run.Geom.s2.Saturation.N = 2.738
run.Geom.s2.Saturation.SRes = 0.0001
run.Geom.s2.Saturation.SSat = 1.0

run.Geom.s3.Saturation.Alpha = 2.692
run.Geom.s3.Saturation.N = 2.445
run.Geom.s3.Saturation.SRes = 0.0001
run.Geom.s3.Saturation.SSat = 1.0

run.Geom.s4.Saturation.Alpha = 0.501
run.Geom.s4.Saturation.N = 2.659
run.Geom.s4.Saturation.SRes = 0.0001
run.Geom.s4.Saturation.SSat = 1.0

run.Geom.s5.Saturation.Alpha = 0.661
run.Geom.s5.Saturation.N = 2.659
run.Geom.s5.Saturation.SRes = 0.0001
run.Geom.s5.Saturation.SSat = 1.0

run.Geom.s6.Saturation.Alpha = 1.122
run.Geom.s6.Saturation.N = 2.479
run.Geom.s6.Saturation.SRes = 0.0001
run.Geom.s6.Saturation.SSat = 1.0

run.Geom.s7.Saturation.Alpha = 2.089
run.Geom.s7.Saturation.N = 2.318
run.Geom.s7.Saturation.SRes = 0.0001
run.Geom.s7.Saturation.SSat = 1.0

run.Geom.s8.Saturation.Alpha = 0.832
run.Geom.s8.Saturation.N = 2.514
run.Geom.s8.Saturation.SRes = 0.0001
run.Geom.s8.Saturation.SSat = 1.0

run.Geom.s9.Saturation.Alpha = 1.585
run.Geom.s9.Saturation.N = 2.413
run.Geom.s9.Saturation.SRes = 0.0001
run.Geom.s9.Saturation.SSat = 1.0

run.Geom.s10.Saturation.Alpha = 3.311
run.Geom.s10.Saturation.N = 2.202
run.Geom.s10.Saturation.SRes = 0.0001
run.Geom.s10.Saturation.SSat = 1.0

run.Geom.s11.Saturation.Alpha = 1.622
run.Geom.s11.Saturation.N = 2.318
run.Geom.s11.Saturation.SRes = 0.0001
run.Geom.s11.Saturation.SSat = 1.0

run.Geom.s12.Saturation.Alpha = 1.514
run.Geom.s12.Saturation.N = 2.259
run.Geom.s12.Saturation.SRes = 0.0001
run.Geom.s12.Saturation.SSat = 1.0

run.Geom.s13.Saturation.Alpha = 1.122
run.Geom.s13.Saturation.N = 2.479
run.Geom.s13.Saturation.SRes = 0.0001
run.Geom.s13.Saturation.SSat = 1.0

#-----------------------------------------------------------------------------
# Time Cycles
#-----------------------------------------------------------------------------

run.Cycle.Names = 'constant'#t rainrec'
run.Cycle.constant.Names = 'alltime'
run.Cycle.constant.alltime.Length = 1
run.Cycle.constant.Repeat = -1

# run.Cycle.rainrec.Names = 'rain rec'
# run.Cycle.rainrec.rain.Length = 10
# run.Cycle.rainrec.rec.Length = 150
# run.Cycle.rainrec.Repeat = -1


#-----------------------------------------------------------------------------
# Boundary Conditions
#-----------------------------------------------------------------------------

run.BCPressure.PatchNames = run.Geom.domain.Patches

# run.Patch.ocean.BCPressure.Type = 'FluxConst'
# run.Patch.ocean.BCPressure.Cycle = 'constant'
# run.Patch.ocean.BCPressure.RefGeom = 'domain'
# run.Patch.ocean.BCPressure.RefPatch = 'ocean'
# run.Patch.ocean.BCPressure.alltime.Value = 0.0

# run.Patch.sink.BCPressure.Type = 'DirEquilRefPatch'
# run.Patch.sink.BCPressure.Cycle = 'constant'
# run.Patch.sink.BCPressure.RefGeom = 'domain'
# run.Patch.sink.BCPressure.RefPatch = 'sink'
# run.Patch.sink.BCPressure.alltime.Value = 0.0

# run.Patch.lake.BCPressure.Type = 'DirEquilRefPatch'
# run.Patch.lake.BCPressure.Cycle = 'constant'
# run.Patch.lake.BCPressure.RefGeom = 'domain'
# run.Patch.lake.BCPressure.RefPatch = 'lake'
# run.Patch.lake.BCPressure.alltime.Value = 0.0

run.Patch.side.BCPressure.Type = 'FluxConst'
run.Patch.side.BCPressure.Cycle = 'constant'
run.Patch.side.BCPressure.alltime.Value = 0.0

run.Patch.bottom.BCPressure.Type = 'FluxConst'
run.Patch.bottom.BCPressure.Cycle = 'constant'
run.Patch.bottom.BCPressure.alltime.Value = 0.0

run.Patch.top.BCPressure.Type = 'OverlandKinematic'
run.Patch.top.BCPressure.Cycle = 'constant'
run.Patch.top.BCPressure.alltime.Value = 0

run.Solver.EvapTransFile = False
#run.Solver.EvapTrans.FileName = filename_pme


#-----------------------------------------------------------------------------
# Topo slopes in x-direction
#-----------------------------------------------------------------------------

run.TopoSlopesX.Type = 'PFBFile'
run.TopoSlopesX.GeomNames = 'domain'
run.TopoSlopesX.FileName = filename_slopex


#-----------------------------------------------------------------------------
# Topo slopes in y-direction
#-----------------------------------------------------------------------------

run.TopoSlopesY.Type = 'PFBFile'
run.TopoSlopesY.GeomNames = 'domain'
run.TopoSlopesY.FileName = filename_slopey


#-----------------------------------------------------------------------------
# Initial conditions: water pressure
#-----------------------------------------------------------------------------

# run.ICPressure.Type = 'HydroStaticPatch'

# if istep == 0:
#     run.ICPressure.GeomNames = 'domain'
#     run.Geom.domain.ICPressure.RefPatch = 'bottom'
#     run.Geom.domain.ICPressure.RefGeom = 'domain'
#     run.Geom.domain.ICPressure.Value = 372.
# else:
run.ICPressure.Type = 'PFBFile'
run.ICPressure.GeomNames = 'domain'
run.Geom.domain.ICPressure.FileName = filename_initialpressure


#-----------------------------------------------------------------------------
# Phase sources:
#-----------------------------------------------------------------------------

run.PhaseSources.water.Type = 'Constant'
run.PhaseSources.water.GeomNames = 'domain'
run.PhaseSources.water.Geom.domain.Value = 0.0

#-----------------------------------------------------------------------------
# Mannings coefficient
#-----------------------------------------------------------------------------

run.Mannings.Type = 'PFBFile'
run.Mannings.FileName = filename_mannings


#-----------------------------------------------------------------------------
# Exact solution specification for error calculations
#-----------------------------------------------------------------------------

run.KnownSolution = 'NoKnownSolution'

#----------------------------------------------------------------
# CLM Settings:
# ------------------------------------------------------------
run.Solver.LSM                   = 'CLM'
#run.Solver.CLM.CLMFileDir        = clm_output_path
run.Solver.CLM.Print1dOut        = False
run.Solver.BinaryOutDir          = False
run.Solver.CLM.CLMDumpInterval   = 1

run.Solver.CLM.MetForcing        = '3D'
run.Solver.CLM.MetFileName       = 'NLDAS'
run.Solver.CLM.MetFilePath       = forcing_path 
run.Solver.CLM.MetFileNT         = 24
run.Solver.CLM.IstepStart        = istep+1

run.Solver.CLM.EvapBeta          = 'Linear'
run.Solver.CLM.VegWaterStress    = 'Saturation'
run.Solver.CLM.ResSat            = 0.2
run.Solver.CLM.WiltingPoint      = 0.2
run.Solver.CLM.FieldCapacity     = 1.00
run.Solver.CLM.IrrigationType    = 'none'

run.Solver.CLM.RootZoneNZ        = 4
run.Solver.CLM.SoiLayer          = 4
run.Solver.CLM.ReuseCount        = int(run.TimingInfo.BaseUnit/run.TimeStep.Value)
run.Solver.CLM.WriteLogs         = False
run.Solver.CLM.WriteLastRST      = True
run.Solver.CLM.DailyRST          = True
run.Solver.CLM.SingleFile        = True

#-----------------------------------------------------------------------------
# Set solver parameters
#-----------------------------------------------------------------------------

run.Solver = 'Richards'
run.Solver.TerrainFollowingGrid = True
run.Solver.TerrainFollowingGrid.SlopeUpwindFormulation = 'Upwind'

run.Solver.SurfacePredictor = True 
run.Solver.SurfacePredictor.PrintValues = True 
run.Solver.SurfacePredictor.PressureValue = 0.00001

run.Solver.MaxIter = 250000
run.Solver.Drop = 1E-30
run.Solver.AbsTol = 1E-9
run.Solver.MaxConvergenceFailures = 20
run.Solver.Nonlinear.MaxIter = 500
run.Solver.Nonlinear.ResidualTol = 1e-7

## new solver settings for Terrain Following Grid
run.Solver.Nonlinear.EtaChoice = 'EtaConstant'
run.Solver.Nonlinear.EtaValue = 0.001
run.Solver.Nonlinear.UseJacobian = True
run.Solver.Nonlinear.DerivativeEpsilon = 1e-16
run.Solver.Nonlinear.StepTol = 1e-16
run.Solver.Nonlinear.Globalization = 'LineSearch'
run.Solver.Linear.KrylovDimension = 500
run.Solver.Linear.MaxRestarts = 8

run.Solver.Linear.Preconditioner = 'PFMG'
run.Solver.Linear.Preconditioner.PCMatrixType = 'PFSymmetric'
run.Solver.WriteSiloPressure = False
run.Solver.PrintSubsurfData = True
run.Solver.PrintMask = True
run.Solver.PrintMannings = True
run.Solver.PrintVelocities = False
run.Solver.PrintPressure = True
run.Solver.PrintSubsurfData = True
run.Solver.PrintSaturation = True
run.Solver.WriteCLMBinary = False
run.Solver.PrintCLM = True
run.Solver.PrintOverlandSum = False

run.Solver.WriteSiloSpecificStorage = False
run.Solver.WriteSiloMannings = False
run.Solver.WriteSiloMask = False
run.Solver.WriteSiloSlopes = False
run.Solver.WriteSiloSubsurfData = False
run.Solver.WriteSiloPressure = False
run.Solver.WriteSiloSaturation = False
run.Solver.WriteSiloEvapTrans = False
run.Solver.WriteSiloEvapTransSum = False
run.Solver.WriteSiloOverlandSum = False
run.Solver.WriteSiloCLM = False

#run.Solver.CLM.UseSlopeAspect = True
run.Reservoirs.Names = 'reservoir'

run.Reservoirs.reservoir.Intake_X = 40.5 * resolution
run.Reservoirs.reservoir.Intake_Y = 20.5 * resolution
run.Reservoirs.reservoir.Release_X = 40.5 * resolution
run.Reservoirs.reservoir.Release_Y = 19.5 * resolution
run.Reservoirs.reservoir.Has_Secondary_Intake_Cell = -1
run.Reservoirs.reservoir.Secondary_Intake_X = -1
run.Reservoirs.reservoir.Secondary_Intake_Y = -1

run.Reservoirs.reservoir.Max_Storage = 10000000000
run.Reservoirs.reservoir.Storage = 0
run.Reservoirs.reservoir.Min_Release_Storage = -10000000000
if RELEASE_WATER:
    #this is the average flow rate just downstream of the reservoir
    run.Reservoirs.reservoir.Release_Rate = 15715.0
else:
    run.Reservoirs.reservoir.Release_Rate = 0

##DISTRIBUTE INPUTS
run.dist(filename_indicator)
run.dist(filename_depthtobedrock)
#run.dist(filename_pme)
run.dist(filename_slopex)
run.dist(filename_slopey)
run.dist(filename_mannings)
run.dist(filename_initialpressure)

#-----------------------------------------------------------------------------------------
# Distribute Forcing
#-----------------------------------------------------------------------------------------
#it will copy and distribute all year of forcing, regardless of no_days
# for filename_forcing in os.listdir(forcing_path):
#     if filename_forcing[-3:]=='pfb':
#         print(f'{forcing_path}{filename_forcing}')
#         if os.path.isfile(f'{forcing_path}{filename_forcing}.dist')==False or redistribute_forcing==True:
#             run.dist(f'{forcing_path}{filename_forcing}')

run.run()

