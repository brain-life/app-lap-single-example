function out = lifeConverter()

addpath(genpath('/N/u/hayashis/BigRed2/git/vistasoft'));
addpath(genpath('/N/u/brlife/git/jsonlab'));
addpath(genpath('/N/u/brlife/git/o3d-code'));
addpath(genpath('/N/u/brlife/git/encode'));

config = loadjson('config.json');
fe_src_moving = fullfile(config.tractogram_moving);
fe_src_static = fullfile(config.tractogram_static);
ref_src_moving = fullfile(config.t1_moving);
ref_src_static = fullfile(config.t1_static);
trk_out_moving = 'life_moving_output.trk';
trk_out_static = 'life_static_output.trk';

% Convert positively-weighted streamlines from LiFE into .trk
fe2trk(fe_src_moving, ref_src_moving, trk_out_moving);
fe2trk(fe_src_static, ref_src_static, trk_out_static);

exit;
end
