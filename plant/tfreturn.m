
function tf1 = tfreturn(k)
    
    load('TFMAIN4.mat')
    field = fieldnames(TF);

    tf = struct;

    name        = field{k};
    tf.name     = name;

    rd          = TF.(name).ResponseData;
    tf.rd       = squeeze(rd);

    tf.ts        = TF.(name).Ts;
    tf.timeunit  = TF.(name).TimeUnit;

    tf.frequency = TF.(name).Frequency;
    tf.frequnit  = TF.(name).FrequencyUnit;   

    tf1 = tf;
end