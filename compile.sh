#!/bin/bash
module load matlab/2017a

cat > build.m <<END
addpath(genpath('/N/u/brlife/git/vistasoft'));
addpath(genpath('/N/u/brlife/git/jsonlab'));
addpath(genpath('/N/u/brlife/git/o3d-code'));
addpath(genpath('/N/u/brlife/git/encode'));
mcc -m -R -nodisplay -d compiled lifeConvereter
mcc -m -R -nodisplay -d compiled my_convert_tck2fg
mcc -m -R -nodisplay -d compiled afqConvverter1

addpath(genpath('/N/u/kitchell/Karst/Applications/mba'))
addpath(genpath('/N/soft/mason/SPM/spm8'))
addpath(genpath('/N/dc2/projects/lifebid/code/kitchell/wma'))
mcc -m -R -nodisplay -d compiled my_fg_merge
exit
END
matlab -nodisplay -nosplash -r build && rm build.m

