%% Modify these parameters
upperBound = 60;
subplotRows = 2;
subplotCols = 2;

%% Code Start
close all;
if(exist("tab", 'var'))
    getTab = questdlg("Table already exists. Choose new table?", ...
            "Choose Table", "Yes", "No", "Yes");
else; getTab = "Yes"; end

if(getTab == "Yes")
    [file, path] = uigetfile({"*.xlsx", "*.csv"});
    tab = readtable(fullfile(path, file), VariableNamingRule = "preserve");
end

creds = ["All Credentials"; unique(tab{:, 'Credentials'})];
credChoices = listdlg(PromptString = "Select a Degree", ListString = creds);

for credIndex = credChoices
    if(credIndex > 1); credTab = tab(tab.Credentials == creds(credIndex), :);
    else; credTab = tab; end
    
    males = credTab{credTab.Gender == "Male", 4:end};
    females = credTab{credTab.Gender == "Female", 4:end};
    
    params = credTab.Properties.VariableNames(4:end);
    fig = figure(Name = creds(credIndex));
    set(fig, 'Position', [50, 0, 1000, 750])
    for paramIndex = 1:length(params)
        subplot(subplotRows, subplotCols, paramIndex);
        hold on;
    
        histogram(males(:, paramIndex), BinWidth = 2);
        histogram(females(:, paramIndex), BinWidth = 2);
        xlim([0, upperBound]);
    
        maleExString = nnz(males(:, paramIndex) > 60);
        if maleExString > 0; maleExString = ", " + maleExString + " not shown";
        else; maleExString = ""; end
    
        femaleExString = nnz(females(:, paramIndex) > 60);
        if femaleExString > 0; femaleExString = ", " + femaleExString + " not shown";
        else; femaleExString = ""; end
        
        title(creds(credIndex) +", " + params{paramIndex});
        xlabel("Number of Publications")
        ylabel("Number of Authors")
        legend("Male Authors (n = " + length(males) + maleExString + ")", ...
            "Female Authors (n = " + length(females) + femaleExString + ")");
    end
    saveas(fig, "Paper Count - " + creds(credIndex) + ".png");
end