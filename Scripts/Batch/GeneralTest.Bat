set P4CLIENT=desktop-jakwonlee


for /f %%C in ('p4 -F %%change%% changes -s pending -c %P4CLIENT%') do (
    p4 -c %P4CLIENT% revert -c %%C //... >nul 2>&1
    p4 shelve -d -c %%C >nul 2>&1
    p4 change -d %%C >nul 2>&1
)