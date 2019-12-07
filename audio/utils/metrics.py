import torch
import numpy as np
import editdistance


def compute_cer(predictionBatch, targetBatch, predictionLenBatch, targetLenBatch):
    targetBatch = targetBatch.cpu()
    targetLenBatch = targetLenBatch.cpu()

    preds = list(torch.split(predictionBatch, predictionLenBatch.tolist()))
    trgts = list(torch.split(targetBatch, targetLenBatch.tolist()))
    totalEdits = 0
    totalChars = torch.sum(targetLenBatch).item()
    
    for n in range(len(preds)):
        pred = preds[n].numpy()
        trgt = trgts[n].numpy()
        numEdits = editdistance.eval(pred, trgt)
        totalEdits = totalEdits + numEdits

    return totalEdits/totalChars



def compute_wer(predictionBatch, targetBatch, predictionLenBatch, targetLenBatch, spaceIx):
    targetBatch = targetBatch.cpu()
    targetLenBatch = targetLenBatch.cpu()
    
    preds = list(torch.split(predictionBatch, predictionLenBatch.tolist()))
    trgts = list(torch.split(targetBatch, targetLenBatch.tolist()))    
    totalEdits = 0
    totalWords = 0
    
    for n in range(len(preds)):
        pred = preds[n].numpy()
        trgt = trgts[n].numpy()

        predWords = np.split(pred, np.where(pred == spaceIx)[0])
        predWords = [predWords[0].tostring()] + [predWords[i][1:].tostring() for i in range(1, len(predWords)) if len(predWords[i][1:]) != 0]

        trgtWords = np.split(trgt, np.where(trgt == spaceIx)[0])
        trgtWords = [trgtWords[0].tostring()] + [trgtWords[i][1:].tostring() for i in range(1, len(trgtWords))]

        numEdits = editdistance.eval(predWords, trgtWords)
        totalEdits = totalEdits + numEdits
        totalWords = totalWords + len(trgtWords)

    return totalEdits/totalWords

