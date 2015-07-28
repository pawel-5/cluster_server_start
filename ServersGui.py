#!/usr/bin/env python

import os 
import Tkinter as tk
import sys
import time
import re


class ServersGui:
    """
    Gui wrapper 
    """
    _servers_ip=[] 
    _window=None
    _module=None
    _edit_splitcount=None
    _splitcount=20
    _extrawigets=[]
    _geometry='500x700'
    _cssh_params={}
    _edit_user=None
    _edit_key=None
    _cmd="cssh  -T \"%s\" -l %s -o \" %s -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \" %s  &"

    def  __init__(self, servers_ip, cssh_params={}):
        """
        Set IPs, params
        """
        print "Found ", len(servers_ip), " groups"
        if len(servers_ip) == 0:
            print "No servers_ip found"
            os.close(1)
        
        self._cssh_params=cssh_params
        server_keys = servers_ip.keys()
        server_keys.sort()
        
        for key in server_keys:
            self._servers_ip.append((key,servers_ip[key]))

        self._startgui()

    def _startgui(self, ):
        """
        Setup window, draw raddio buttons
        """
        self._window=tk.Tk()
        self._window.geometry(self._geometry)
        self._window.title('Servers')

        tk.Label( self._window, text="Servers per page").grid(row=0, column=0)
        self._edit_splitcount=tk.Entry(self._window, width=40)
        self._edit_splitcount.grid(row=0, column=1)
        self._edit_splitcount.insert(0, str(self._splitcount) )
        
        ystart=50
        # add modules to frame
        self._module = tk.IntVar()
        i=1
        for group in self._servers_ip:
            w=tk.Radiobutton(self._window, text=group[0]+" ["+str( len(group[1]) )+']', 
                             variable=self._module, value=i, command=self.moduleselected)
            w.place(x=10, y=25*i+ystart)
            i+=1

        self._window.mainloop()
        
    def _get_comand(self, name, user, key_file, ips):
        """
        Expend cssh command 
        """
        if key_file:
            key_file = "-i %s " % key_file

        return self._cmd % (name , user , key_file, ips)
        
    def moduleselected(self):
        """
        Callback for radiobutton click, drawing "page" button
        """
        for w in self._extrawigets:
            w.destroy()
 
        module=self._servers_ip[self._module.get()-1]
         
        c =  self._find_user_key(module[0])
        y=50
        label1 = tk.Label(self._window, text="User:")
        label1.grid(row=1, column=0)
        self._edit_user=tk.Entry(self._window,width=40)
        self._edit_user.grid(row=1, column=1)
        self._edit_user.insert(0, c[0] )

        y+=30 
        label2 = tk.Label(self._window, text="Key:")
        label2.grid(row=2, column=0)
        self._edit_key=tk.Entry(self._window,width=40)
        self._edit_key.grid(row=2, column=1)
        self._edit_key.insert(0, c[1] )
 
        count=len(module[1])
        pages=count/float(self._splitcount)
        
        try:
            self._splitcount= int(self._edit_splitcount.get())
        except:
            self._splitcount=20
            None
        
        if pages > 1.0:
            extra = 1
            if pages == count/self._splitcount:
                extra = 0
            for i in range(int(pages)+extra):
                w=tk.Button( self._window, text="Page "+str(i+1), command= lambda i=i: self._moduleexec(i) )
                w.place(x=300, y=(y+(30*i)))
                self._extrawigets.append(w)

            i+=2
            w=tk.Button( self._window, text="All", command= lambda i=i: self._moduleexec(-1) )
            w.place(x=300, y=(y+(30*i)))
            self._extrawigets.append(w)

        else:
            i=0
            w=tk.Button( self._window, text="All", command= lambda i=i: self._moduleexec(i))
            w.place(x=300, y=y)
            self._extrawigets.append(w)
            
    def _find_user_key(self, value):
        """
        Find user and key for ssh connection 
        if nothing is matching use current user without key
        """
        for k, v in self._cssh_params.iteritems():
            if k != "" and re.match( r''+k, value, re.I):
                return v

        if self._cssh_params.get(""):
            return self._cssh_params[""]

        return (os.environ['USER'] , "")

    def _moduleexec(self, i):
        """
        Build exec module
        """
        ip=''
        module=self._servers_ip[self._module.get()-1]
        ips=module[1]

        if i==0:
            ip=ips[0:self._splitcount]
        elif (len(ips)/self._splitcount) == i:
            ip=ips[i*self._splitcount:]
        else:
            ip=ips[i*self._splitcount:(i+1)*self._splitcount]

        name=module[0]+"_"+str(time.time())
        
        key_file = self._edit_key.get()
        if key_file:
            key_file = "-i %s " % key_file
        
        cmd = self._cmd % ( name, self._edit_user.get(), key_file, " ".join(ip))
        print cmd
        os.system( cmd )
        
        self._window.destroy()
        sys.exit()

if __name__ == "__main__":
    # python map where key is "tag" name  and value array of IPs
    servers_ip={'x2':['ip1','ip2','ip3'],'s1':['ip5','ip6']}
    # python map where key is tag name  and value is tuple with (user, keyfile)
    cssh_params = {'': ('user', 'key'),'s': ('users', 'key1')}
    ServersGui(servers_ip,  cssh_params)



