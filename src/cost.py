import control as ct
from vibration import Margin
import numpy as np


class Cost(object):
    """
    run input > controller_frd, plants_frd, freq_rad
    output    > total_cost
    """

    class CostData(object):
        def __init__(self, gm, ph, wg, bw, ol_mag, etf_mag):
            self.gm      = gm
            self.ph      = ph
            self.wg      = wg
            self.bw      = bw # wp is bandwidth where gain is 0db
            self.ol_mag  = ol_mag
            self.etf_mag = etf_mag

    def __init__(self, margin_obj, plant_obj):
        
        self.margin_obj = margin_obj
        self.plant_obj  = plant_obj

    # returns Margin.MAXIMUM if approaches infinity
    def run(self, controller_frd):
        
        pln = self.plant_obj.frd    # plant frd
        frq = self.plant_obj.freq   # frequncy rad
        num = self.plant_obj.length # plant number

        cnt = controller_frd        # controller frd
       
        cost_data = []
        for k in range(num): 
            cd = Cost.margin_cal(cnt, pln[k], frq)
            if cd is None:
                return Margin.MAXIMUM

            cost_data.append(cd) # appending objects
        
        total_cost = self.cost_cal(cost_data)
        return total_cost


    # returns None if approaches infinity
    @staticmethod
    def margin_cal(cont_frd, plant, freq):
        # open loop
        ol_frd = cont_frd * plant
        gm1, ph1, wg1, wp1 = ct.margin(ol_frd)    

        if (gm1 > 100) or (ph1 > 150) or (ph1 < 1) or (wp1 is None):
            return None

        ol_rsp  = ol_frd.freqresp(freq)
        ol_mag = list(ol_rsp[0][0][0])
        
        # error transfer function
        etf_frd = 1/(1 + ol_frd)
        etf_rsp = etf_frd.freqresp(freq)
        etf_mag = list(etf_rsp[0][0][0])

        return Cost.CostData(gm1, ph1, wg1, wp1, ol_mag, etf_mag)


    def cost_cal(self, cost_data): 

            gmt     = self.margin_obj.gmt   
            gmw     = self.margin_obj.gmw
            pht     = self.margin_obj.pht  
            phw     = self.margin_obj.phw   
           
            bwt     = self.margin_obj.bwt
            bww     = self.margin_obj.bww

            oltv    = self.margin_obj.olub_tv
            olwv    = self.margin_obj.olub_wv

            etftv   = self.margin_obj.etfub_tv
            etfwv   = self.margin_obj.etfub_wv

            pllen   = self.plant_obj.length
            freqlen = self.plant_obj.freqlen
            
            total_cost  = []
            for i in  range(pllen):
                cost = 0
                ph      = cost_data[i].ph   
                gm      = cost_data[i].gm    
                bw      = cost_data[i].bw  

                ol_mag  = cost_data[i].ol_mag
                etf_mag = cost_data[i].etf_mag

                if gm < gmt:
                    cost += gmw*((gm - gmt)/gmt)**2

                if ph < pht:
                    cost += phw*((ph - pht)/pht)**2

                if bw < bwt:
                    cost += bww*((bw - bwt)/bwt)**2


                for i in range(freqlen):
                    if etf_mag[i] > etftv[i]: 
                        cost += etfwv[i]*((etf_mag[i]-etftv[i])/etftv[i])**2
                    
                    if ol_mag[i] > ol_mag[i]:
                        cost +=  olwv[i]*((ol_mag[i] - oltv[i])/oltv[i])**2


                total_cost.append(cost)
            
            return sum(total_cost)





if __name__ == '__main__': 
    
    from vibration import Const, Plant, Controller, ControlParam

    mypl = Plant()
    mypl.run(Const.PLANT_PATH)

    mymrg = Margin()
    mymrg.run(mypl.freqhz, mypl.freqhzunit)
    
    # IN THIS SCRIPT
    mycost = Cost(mymrg, mypl)   
    myct= Controller(mypl.freq)
    
    def IO(x): 
        ctfrd = myct.run(x)
        total_cost = mycost.run(ctfrd)
        print('total cost is')
        print(total_cost)

    IO(ControlParam.x_am_matlab)
