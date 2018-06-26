function out = afqConverter1()

if ~isdeployed
	addpath(genpath('/N/u/brlife/git/vistasoft'));
	addpath(genpath('/N/u/brlife/git/jsonlab'));
	addpath(genpath('/N/u/brlife/git/o3d-code'));
end

config = loadjson('config.json');
ref_src = fullfile(config.t1_moving);

%convert afq to trk
disp('Converting afq to .trk');

%sub1
load(fullfile(config.segmentation));
fid=fopen('tract_name_list.txt', 'w');

if (config.tract1 > 0)
    for tract = [config.tract1, config.tract2, config.tract3, config.tract4, config.tract5, config.tract6, config.tract7, config.tract8]
        if (tract > 0)
            tract_name=strrep(fg_classified(tract).name,' ','_');
            write_fg_to_trk(fg_classified(tract),ref_src,sprintf('%s_tract.trk',tract_name));
            fprintf(fid, [tract_name, '\n']);
        end    
    end  
  
elseif length(fg_classified) == 20
    disp('AFQ segmentation selected. The plots of the following tracts will be returned:')
    disp('Left and Right Thalamic Radiation, Left and Rigth Corticospinal, Left and Right IFOF, Left and Right Arcuate.')
    for tract = [1, 2, 3, 4, 11, 12, 19, 20]
	tract_name=strrep(fg_classified(tract).name,' ','_');
        write_fg_to_trk(fg_classified(tract),ref_src,sprintf('%s_tract.trk',tract_name));
        fprintf(fid, [tract_name, '\n']);
    end

elseif length(fg_classified) == 79
    disp('Wma segmentation selected. The plots of the following tracts will be returned:')
    disp('Left and Rigth pArc, Left and Rigth TPC, Left and Rigth MdLF-SPL, Left and Rigth MdLF-Ang.')
    for tract = [38, 39, 40, 41, 42, 43, 44, 45]
	tract_name=strrep(fg_classified(tract).name,' ','_');
        write_fg_to_trk(fg_classified(tract),ref_src,sprintf('%s_tract.trk',tract_name));
        fprintf(fid, [tract_name, '\n']);
    end
end
 

fclose(fid);

exit;
end
