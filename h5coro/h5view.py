# Copyright (c) 2023, University of Washington
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the University of Washington nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF WASHINGTON AND CONTRIBUTORS
# “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF WASHINGTON OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from h5coro.h5promise import massagePath

###############################################################################
# H5View Class
###############################################################################

class H5View:

    #######################
    # Constructor
    #######################
    def __init__(self, promise, path=""):
        self.promise = promise
        self.path = massagePath(path)
        self.datasets = {}
        for dataset in promise.datasets:
            if dataset.startswith(self.path):
                subpath = massagePath(dataset[len(self.path):])
                if len(subpath) > 0:
                    element = list(filter(('').__ne__, subpath.split('/')))[0]
                    if element not in self.datasets:
                        newpath = self.path + "/" + element
                        self.datasets[element] = H5View(promise, path=newpath)

    #######################
    # operator: []
    #######################
    def __getitem__(self, key):
        key = massagePath(key)
        fullpath = self.path + "/" + key
        if fullpath in self.promise.datasets:
            return self.promise[fullpath]
        else:
            return self.datasets[key]

    #######################
    # representation
    #######################
    def __repr__(self):
        repr = []
        self.display(self, 0, repr)
        return ''.join(repr)

    #######################
    # string
    #######################
    def __str__(self):
        return self.__repr__()

    #######################
    # iterate
    #######################
    def __iter__(self):
        for key in self.datasets.keys():
            yield key

    #######################
    # keys
    #######################
    def keys(self):
        return self.datasets.keys()

    #######################
    # display
    #######################
    def display(self, view, lvl, repr):
        space = '    '*lvl
        for key in view.keys():
            repr.append(f'{space}{key}\n')
            if type(view[key]) == H5View:
                self.display(view[key], lvl+1, repr)
