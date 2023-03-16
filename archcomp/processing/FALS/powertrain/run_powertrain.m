function [tout, yout] = run_powertrain(u, T)
    
    assignin('base','u',u);
    assignin('base','T',T);
    
    result = sim('AbstractFuelControl_M1', ...
        'StopTime', 'T', ...
        'LoadExternalInput', 'on', 'ExternalInput', 'u', ...
        'SaveTime', 'on', 'TimeSaveName', 'tout', ...
        'SaveOutput', 'on', 'OutputSaveName', 'yout', ...
        'SaveFormat', 'Array');
    tout = result.tout;
    yout = result.yout;
end
