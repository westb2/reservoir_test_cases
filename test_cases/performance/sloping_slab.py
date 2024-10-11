
import sys, argparse
from parflow import Run
import parflow as pf
import numpy as np
from parflow.tools.fs import mkdir, get_absolute_path, rm
from parflow.tools.compare import pf_test_file
from parflow.tools.builders import ReservoirPropertiesBuilder

def run_model(number_of_reservoirs, rain_condition, reservoir_condition):
    overland = Run("performance", __file__)

    model_location = f"sloping_slab_with_{number_of_reservoirs}_reservoirs_{reservoir_condition}_{rain_condition}"

    new_output_dir_name = get_absolute_path('test_output_longer_run/' + model_location)
    mkdir(new_output_dir_name)
    with open(new_output_dir_name+"/start_file.txt", "w") as file:
        file.write("starting")

    #---------------------------------------------------------

    overland.FileVersion = 4

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-p', '--p', default=1)
    # parser.add_argument('-q', '--q', default=1)
    # parser.add_argument('-r', '--r', default=1)
    # args = parser.parse_args()

    overland.Process.Topology.P = 1 #args.p
    overland.Process.Topology.Q = 1 #args.q
    overland.Process.Topology.R = 1 #args.r

    #---------------------------------------------------------
    # Computational Grid
    #---------------------------------------------------------

    overland.ComputationalGrid.Lower.X = 0.0
    overland.ComputationalGrid.Lower.Y = 0.0
    overland.ComputationalGrid.Lower.Z = 0.0


    nx, ny, nz = 500,500,1
    overland.ComputationalGrid.NX = nx
    overland.ComputationalGrid.NY = ny
    overland.ComputationalGrid.NZ = nz

    dx, dy, dz = 10.0,10.0,.05
    overland.ComputationalGrid.DX = dx
    overland.ComputationalGrid.DY = dy
    overland.ComputationalGrid.DZ = dz

    #---------------------------------------------------------
    # The Names of the GeomInputs
    #---------------------------------------------------------

    overland.GeomInput.Names = 'domaininput'
    overland.GeomInput.domaininput.GeomName = 'domain'
    overland.GeomInput.domaininput.InputType = 'Box'

    #---------------------------------------------------------
    # Domain Geometry
    #---------------------------------------------------------

    overland.Geom.domain.Lower.X = 0.0
    overland.Geom.domain.Lower.Y = 0.0
    overland.Geom.domain.Lower.Z = 0.0

    overland.Geom.domain.Upper.X = nx*dx
    overland.Geom.domain.Upper.Y = ny*dy
    overland.Geom.domain.Upper.Z = nz*dz
    overland.Geom.domain.Patches = 'x_lower x_upper y_lower y_upper z_lower z_upper'

    slope_x = np.ones([1,ny,nx])*-.01
    slope_y = np.ones([1,ny,nx])*0
    pf.write_pfb("input_files/slope_x.pfb", slope_x)
    pf.write_pfb("input_files/slope_y.pfb", slope_y)
    #-----------------------------------------------------------------------------
    # Perm
    #-----------------------------------------------------------------------------

    overland.Geom.Perm.Names = 'domain'
    overland.Geom.domain.Perm.Type = 'Constant'
    overland.Geom.domain.Perm.Value = 0.0000001

    overland.Perm.TensorType = 'TensorByGeom'

    overland.Geom.Perm.TensorByGeom.Names = 'domain'

    overland.Geom.domain.Perm.TensorValX = 1.0
    overland.Geom.domain.Perm.TensorValY = 1.0
    overland.Geom.domain.Perm.TensorValZ = 1.0

    #-----------------------------------------------------------------------------
    # Specific Storage
    #-----------------------------------------------------------------------------

    overland.SpecificStorage.Type = 'Constant'
    overland.SpecificStorage.GeomNames = 'domain'
    overland.Geom.domain.SpecificStorage.Value = 1.0e-4

    #-----------------------------------------------------------------------------
    # Phases
    #-----------------------------------------------------------------------------

    overland.Phase.Names = 'water'

    overland.Phase.water.Density.Type = 'Constant'
    overland.Phase.water.Density.Value = 1.0

    overland.Phase.water.Viscosity.Type = 'Constant'
    overland.Phase.water.Viscosity.Value = 1.0

    #-----------------------------------------------------------------------------
    # Contaminants
    #-----------------------------------------------------------------------------

    overland.Contaminants.Names = ''

    #-----------------------------------------------------------------------------
    # Retardation
    #-----------------------------------------------------------------------------

    overland.Geom.Retardation.GeomNames = ''

    #-----------------------------------------------------------------------------
    # Gravity
    #-----------------------------------------------------------------------------

    overland.Gravity = 1.0

    #-----------------------------------------------------------------------------
    # Setup timing info
    #-----------------------------------------------------------------------------

    overland.TimingInfo.BaseUnit = 0.05
    overland.TimingInfo.StartCount = 0
    overland.TimingInfo.StartTime = 0.0
    overland.TimingInfo.StopTime = 10.0
    overland.TimingInfo.DumpInterval = 1.0
    overland.TimeStep.Type = 'Constant'
    overland.TimeStep.Value = 0.05

    #-----------------------------------------------------------------------------
    # Porosity
    #-----------------------------------------------------------------------------

    overland.Geom.Porosity.GeomNames = 'domain'
    overland.Geom.domain.Porosity.Type = 'Constant'
    overland.Geom.domain.Porosity.Value = 0.01

    #-----------------------------------------------------------------------------
    # Domain
    #-----------------------------------------------------------------------------

    overland.Domain.GeomName = 'domain'

    #-----------------------------------------------------------------------------
    # Relative Permeability
    #-----------------------------------------------------------------------------

    overland.Phase.RelPerm.Type = 'VanGenuchten'
    overland.Phase.RelPerm.GeomNames = 'domain'

    overland.Geom.domain.RelPerm.Alpha = 6.0
    overland.Geom.domain.RelPerm.N = 2.

    #---------------------------------------------------------
    # Saturation
    #---------------------------------------------------------

    overland.Phase.Saturation.Type = 'VanGenuchten'
    overland.Phase.Saturation.GeomNames = 'domain'

    overland.Geom.domain.Saturation.Alpha = 6.0
    overland.Geom.domain.Saturation.N = 2.
    overland.Geom.domain.Saturation.SRes = 0.2
    overland.Geom.domain.Saturation.SSat = 1.0

    #-----------------------------------------------------------------------------
    # Wells
    #-----------------------------------------------------------------------------

    overland.Wells.Names = ''

    #-----------------------------------------------------------------------------
    # Time Cycles
    #-----------------------------------------------------------------------------

    overland.Cycle.Names = 'constant rainrec'
    overland.Cycle.constant.Names = 'alltime'
    overland.Cycle.constant.alltime.Length = 1
    overland.Cycle.constant.Repeat = -1

    # rainfall and recession time periods are defined here
    # rain for 1 hour, recession for 2 hours

    overland.Cycle.rainrec.Names = 'rain rec'
    overland.Cycle.rainrec.rain.Length = 1
    overland.Cycle.rainrec.rec.Length = 1
    overland.Cycle.rainrec.Repeat = -1

    #-----------------------------------------------------------------------------
    # Boundary Conditions: Pressure
    #-----------------------------------------------------------------------------

    overland.BCPressure.PatchNames = overland.Geom.domain.Patches

    overland.Patch.x_lower.BCPressure.Type = 'FluxConst'
    overland.Patch.x_lower.BCPressure.Cycle = 'constant'
    overland.Patch.x_lower.BCPressure.alltime.Value = 0.0

    overland.Patch.y_lower.BCPressure.Type = 'FluxConst'
    overland.Patch.y_lower.BCPressure.Cycle = 'constant'
    overland.Patch.y_lower.BCPressure.alltime.Value = 0.0

    overland.Patch.z_lower.BCPressure.Type = 'FluxConst'
    overland.Patch.z_lower.BCPressure.Cycle = 'constant'
    overland.Patch.z_lower.BCPressure.alltime.Value = 0.0

    overland.Patch.x_upper.BCPressure.Type = 'FluxConst'
    overland.Patch.x_upper.BCPressure.Cycle = 'constant'
    overland.Patch.x_upper.BCPressure.alltime.Value = 0.0

    overland.Patch.y_upper.BCPressure.Type = 'FluxConst'
    overland.Patch.y_upper.BCPressure.Cycle = 'constant'
    overland.Patch.y_upper.BCPressure.alltime.Value = 0.0

    ## overland flow boundary condition with very heavy rainfall then slight ET
    overland.Patch.z_upper.BCPressure.Type = 'OverlandKinematic'
    overland.Patch.z_upper.BCPressure.Cycle = 'rainrec'
    if rain_condition == "constant_rain":
        overland.Patch.z_upper.BCPressure.rain.Value = -0.01
        overland.Patch.z_upper.BCPressure.rec.Value = -0.01
    elif rain_condition == "periodic_rainfall":
        overland.Patch.z_upper.BCPressure.rain.Value = -0.01
        overland.Patch.z_upper.BCPressure.rec.Value = 0.0000
    elif rain_condition == "no_rain":
        overland.Patch.z_upper.BCPressure.rain.Value = -0.00
        overland.Patch.z_upper.BCPressure.rec.Value = 0.0000



    # add the reservoirs
    overland.Reservoirs.Overland_Flow_Solver = "OverlandKinematic"
    reservoirs_file_location = get_absolute_path(f"reservoir_files/{number_of_reservoirs}_reservoirs_{reservoir_condition}.csv")
    builder = ReservoirPropertiesBuilder(overland).load_csv_file(reservoirs_file_location)
    builder.apply(name_registration=True, infer_key_names=True)
        
    # overland.Reservoirs.Names = 'reservoir1 reservoir2'
    # overland.Reservoirs.reservoir1.Intake_X = 12.5
    # overland.Reservoirs.reservoir1.Intake_Y = 13.5
    # overland.Reservoirs.reservoir1.Release_X = 13.5
    # overland.Reservoirs.reservoir1.Release_Y = 13.5
    # overland.Reservoirs.reservoir1.Has_Secondary_Intake_Cell = -1
    # overland.Reservoirs.reservoir1.Secondary_Intake_X = -1
    # overland.Reservoirs.reservoir1.Secondary_Intake_Y = -1

    # overland.Reservoirs.reservoir1.Max_Storage = 10000
    # overland.Reservoirs.reservoir1.Storage = 5000
    # overland.Reservoirs.reservoir1.Min_Release_Storage = 0
    # overland.Reservoirs.reservoir1.Release_Rate = 1



    # overland.Reservoirs.reservoir2.Intake_X = 22.5
    # overland.Reservoirs.reservoir2.Intake_Y = 13.5
    # overland.Reservoirs.reservoir2.Release_X = 23.5
    # overland.Reservoirs.reservoir2.Release_Y = 13.5
    # overland.Reservoirs.reservoir2.Has_Secondary_Intake_Cell = -1
    # overland.Reservoirs.reservoir2.Secondary_Intake_X = -1
    # overland.Reservoirs.reservoir2.Secondary_Intake_Y = -1

    # overland.Reservoirs.reservoir2.Max_Storage = 10000
    # overland.Reservoirs.reservoir2.Storage = 5000
    # overland.Reservoirs.reservoir2.Min_Release_Storage = 0
    # overland.Reservoirs.reservoir2.Release_Rate = 1


    #---------------------------------------------------------
    # Mannings coefficient
    #---------------------------------------------------------

    overland.Mannings.Type = 'Constant'
    overland.Mannings.GeomNames = 'domain'
    overland.Mannings.Geom.domain.Value = 3.e-6

    #-----------------------------------------------------------------------------
    # Phase sources:
    #-----------------------------------------------------------------------------

    overland.PhaseSources.water.Type = 'Constant'
    overland.PhaseSources.water.GeomNames = 'domain'
    overland.PhaseSources.water.Geom.domain.Value = 0.0

    #-----------------------------------------------------------------------------
    # Exact solution specification for error calculations
    #-----------------------------------------------------------------------------

    overland.KnownSolution = 'NoKnownSolution'

    #-----------------------------------------------------------------------------
    # Set solver parameters
    #-----------------------------------------------------------------------------

    overland.Solver = 'Richards'
    overland.Solver.MaxIter = 2500

    overland.Solver.Nonlinear.MaxIter = 50
    overland.Solver.Nonlinear.ResidualTol = 1e-9
    overland.Solver.Nonlinear.EtaChoice = 'EtaConstant'
    overland.Solver.Nonlinear.EtaValue = 0.01
    overland.Solver.Nonlinear.UseJacobian = False

    overland.Solver.Nonlinear.DerivativeEpsilon = 1e-15
    overland.Solver.Nonlinear.StepTol = 1e-20
    overland.Solver.Nonlinear.Globalization = 'LineSearch'
    overland.Solver.Linear.KrylovDimension = 20
    overland.Solver.Linear.MaxRestart = 5

    overland.Solver.Linear.Preconditioner = 'PFMG'
    overland.Solver.PrintSubsurf = False
    overland.Solver.Drop = 1E-20
    overland.Solver.AbsTol = 1E-10

    overland.Solver.OverlandKinematic.Epsilon = 1E-5

    overland.Solver.WriteSiloSubsurfData = False
    overland.Solver.WriteSiloPressure = False
    overland.Solver.WriteSiloSlopes = False

    overland.Solver.WriteSiloSaturation = False
    overland.Solver.WriteSiloConcentration = False

    #---------------------------------------------------------
    # Initial conditions: water pressure
    #---------------------------------------------------------

    # set water table to be at the top of the domain
    overland.ICPressure.Type = 'HydroStaticPatch'
    overland.ICPressure.GeomNames = 'domain'
    overland.Geom.domain.ICPressure.Value = 0.00

    # overland.ICPressure.Type = 'PFBFile'
    # overland.ICPressure.GeomNames = 'domain'
    # overland.Geom.domain.ICPressure.FileName = get_absolute_path('test_output/sloping_slab/model.out.press.00009.pfb')

    overland.Geom.domain.ICPressure.RefGeom = 'domain'
    overland.Geom.domain.ICPressure.RefPatch = 'z_upper'

    overland.TopoSlopesY.Type = "PFBFile"
    overland.TopoSlopesY.GeomNames = "domain"
    overland.TopoSlopesY.FileName = "/Users/ben/Documents/GitHub/parflow-models/code/models/performance/input_files/slope_y.pfb"

    overland.TopoSlopesX.Type = "PFBFile"
    overland.TopoSlopesX.GeomNames = "domain"
    overland.TopoSlopesX.FileName = "/Users/ben/Documents/GitHub/parflow-models/code/models/performance/input_files/slope_x.pfb"

    # overland.TopoSlopesX.Type  = "Constant"
    # overland.TopoSlopesX.GeomNames = "domain"
    # overland.TopoSlopesX.Geom.domain.Value = -0.01

    # overland.TopoSlopesY.Type = "Constant"
    # overland.TopoSlopesY.GeomNames = "domain"
    # overland.TopoSlopesY.Geom.domain.Value = 0

    overland.Patch.z_upper.BCPressure.Type = 'OverlandKinematic'
    overland.Solver.Nonlinear.UseJacobian = True
    overland.Solver.Linear.Preconditioner.PCMatrixType = 'PFSymmetric'

    run_name = f"model"
    overland.set_name(run_name)



    overland.run(working_directory=new_output_dir_name)
