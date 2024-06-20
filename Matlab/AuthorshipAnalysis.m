close all;

[file, path] = uigetfile({"*.xlsx", "*.csv"});
table = readtable(fullfile(path, file), VariableNamingRule = 'preserve');

paramNames = ["Author Position", "Group Size"];
upperBounds = [20, 50];
suffixes = ["", "_1", "_2", "_3"];

for paramIndex = 1:length(paramNames)
    fig = figure("Name", paramNames(paramIndex));
    set(fig, "Position", [150, 250, 1000 350])
    titles = ["Pre-ERAS " + paramNames(paramIndex) + "s", ...
        "Post-ERAS " + paramNames(paramIndex) + "s"];
    
    for prePost = 1:2
        subplot(1,2,prePost);
        hold on;
        males = table.(paramNames(paramIndex) + suffixes(2 * prePost - 1));
        females = table.(paramNames(paramIndex) + suffixes(2 * prePost));

        histogram(males , BinWidth = 1);
        histogram(females, BinWidth = 1);
        xlim([0, upperBounds(paramIndex)]);
        
        title(titles(prePost));
        xlabel(paramNames(paramIndex));
        ylabel("Number of Papers");
        legend("Male Papers " + nString(males, upperBounds(paramIndex)), ...
            "Female Papers " + nString(females, upperBounds(paramIndex)));
    end
    saveas(fig, "Author Analysis - " + paramNames(paramIndex) + ".png");
end

function nString = nString(data, bound)
    exString = nnz(data > bound);
    if exString > 0; exString = ", " + exString + " not shown";
    else; exString = ""; end
    nString = "(n = " + nnz(~isnan(data)) + exString + ")";
end