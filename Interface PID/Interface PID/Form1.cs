using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Interface_PID
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void buttonStart_Click(object sender, EventArgs e)
        {
            serialPort1.PortName = "COM22";
            serialPort1.BaudRate = 115200;

            serialPort1.Open();
            if (serialPort1.IsOpen)
            {
                buttonStart.Enabled = false;
                buttonStop.Enabled = true;
            }
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                serialPort1.Close();
                buttonStart.Enabled = true;
                buttonStop.Enabled = false;
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.Close();
        }

        private void numericUpDown_angle_ValueChanged(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#set_angle_boussole;" + numericUpDown_angle.Value.ToString() + ";");
        }

        private void numericUpDown_kp_ValueChanged(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#kp;" + numericUpDown_kp.Value.ToString() + ";");
        }

        private void numericUpDown_kd_ValueChanged(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#kd;" + numericUpDown_kd.Value.ToString() + ";");
        }

        private void numericUpDown_ki_ValueChanged(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#ki;" + numericUpDown_ki.Value.ToString() + ";");
        }

        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            serialPort1.ReadLine();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#straight;");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#stop;");
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen) serialPort1.WriteLine("#calibrage;");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            if (serialPort1.IsOpen)
            {
                serialPort1.WriteLine(
                    "#ki;" + numericUpDown_ki.Value.ToString() + ";"
                    + "#kd;" + numericUpDown_kd.Value.ToString() + ";"
                    + "#kp;" + numericUpDown_kp.Value.ToString() + ";");
            }
        }
    }
}
