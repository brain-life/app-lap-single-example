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

% Convert segmentation
load(fullfile(config.segmentation));
for tract = [config.tract1, config.tract2, config.tract3, config.tract4]
    if (tract != "null")
        tract_name=strrep(fg_classified(tract).name,' ','_');
        write_fg_to_trk(fg_classified(tract),ref_src_moving,sprintf('%s_tract.trk',tract_name));
	fid=fopen('tract_name_list.txt', 'w');
	fprintf(fid, [tract, '\n']);
    end
end

fclose(fid);

exit;
end
