function my_convert_tck2fg(tck_filename, tract_name)

if ~isdeployed
	addpath(genpath('/N/u/brlife/git/vistasoft'));
end

fg_classified = dtiImportFibersMrtrix(tck_filename, 0.2, 0.5);
fgWrite(fg_classified, tract_name, 'mat');

exit;
end

