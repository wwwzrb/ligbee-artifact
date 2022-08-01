#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Rpp0 Txrx Usrp
# Generated: Tue Feb 19 12:08:35 2019
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import lora
import time
import wx


class rpp0_txrx_usrp(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Rpp0 Txrx Usrp")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 1
        self.spreading_factor = spreading_factor = 7
        self.samp_rate = samp_rate = 1e6
        self.rx_gain = rx_gain = 1
        self.offset = offset = 0e6
        self.frequency = frequency = 868e6
        self.bw = bw = 500e3

        ##################################################
        # Blocks
        ##################################################
        _tx_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._tx_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_tx_gain_sizer,
        	value=self.tx_gain,
        	callback=self.set_tx_gain,
        	label='tx_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._tx_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_tx_gain_sizer,
        	value=self.tx_gain,
        	callback=self.set_tx_gain,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_tx_gain_sizer)
        _rx_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rx_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rx_gain_sizer,
        	value=self.rx_gain,
        	callback=self.set_rx_gain,
        	label='rx_gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rx_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rx_gain_sizer,
        	value=self.rx_gain,
        	callback=self.set_rx_gain,
        	minimum=0,
        	maximum=1,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rx_gain_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('addr=192.168.10.2', '')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(frequency, 0)
        self.uhd_usrp_source_0.set_normalized_gain(rx_gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('addr=192.168.10.1', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(frequency, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(tx_gain, 0)
        self.lora_message_socket_source_0 = lora.message_socket_source("127.0.0.1", 40868)
        self.lora_lora_receiver_0 = lora.lora_receiver(samp_rate, frequency, ([frequency+offset]), 125000, spreading_factor, False, 4, False, False, False, 1, True, False)
        self.lora_encoder_0 = lora.encoder()
        self._bw_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.bw,
        	callback=self.set_bw,
        	label='bw',
        	converter=forms.float_converter(),
        )
        self.Add(self._bw_text_box)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_message_socket_source_0, 'out'), (self.lora_encoder_0, 'in'))
        self.connect((self.lora_encoder_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.lora_lora_receiver_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self._tx_gain_slider.set_value(self.tx_gain)
        self._tx_gain_text_box.set_value(self.tx_gain)
        self.uhd_usrp_sink_0.set_normalized_gain(self.tx_gain, 0)


    def get_spreading_factor(self):
        return self.spreading_factor

    def set_spreading_factor(self, spreading_factor):
        self.spreading_factor = spreading_factor
        self.lora_lora_receiver_0.set_sf(self.spreading_factor)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self._rx_gain_slider.set_value(self.rx_gain)
        self._rx_gain_text_box.set_value(self.rx_gain)
        self.uhd_usrp_source_0.set_normalized_gain(self.rx_gain, 0)


    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency)
        self.uhd_usrp_source_0.set_center_freq(self.frequency, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.frequency, 0)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self._bw_text_box.set_value(self.bw)


def main(top_block_cls=rpp0_txrx_usrp, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
