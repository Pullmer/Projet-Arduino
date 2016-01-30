namespace Interface_PID
{
    partial class Form1
    {
        /// <summary>
        /// Variable nécessaire au concepteur.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Nettoyage des ressources utilisées.
        /// </summary>
        /// <param name="disposing">true si les ressources managées doivent être supprimées ; sinon, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Code généré par le Concepteur Windows Form

        /// <summary>
        /// Méthode requise pour la prise en charge du concepteur - ne modifiez pas
        /// le contenu de cette méthode avec l'éditeur de code.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.buttonStart = new System.Windows.Forms.Button();
            this.buttonStop = new System.Windows.Forms.Button();
            this.serialPort1 = new System.IO.Ports.SerialPort(this.components);
            this.numericUpDown_kp = new System.Windows.Forms.NumericUpDown();
            this.numericUpDown_kd = new System.Windows.Forms.NumericUpDown();
            this.numericUpDown_ki = new System.Windows.Forms.NumericUpDown();
            this.numericUpDown_angle = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_kp)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_kd)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_ki)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_angle)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(35, 12);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(19, 13);
            this.label1.TabIndex = 3;
            this.label1.Text = "kp";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(32, 38);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(19, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "kd";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(32, 66);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(15, 13);
            this.label3.TabIndex = 5;
            this.label3.Text = "ki";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(21, 94);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(33, 13);
            this.label4.TabIndex = 7;
            this.label4.Text = "angle";
            // 
            // buttonStart
            // 
            this.buttonStart.Location = new System.Drawing.Point(48, 129);
            this.buttonStart.Name = "buttonStart";
            this.buttonStart.Size = new System.Drawing.Size(75, 23);
            this.buttonStart.TabIndex = 12;
            this.buttonStart.Text = "Connect";
            this.buttonStart.UseVisualStyleBackColor = true;
            this.buttonStart.Click += new System.EventHandler(this.buttonStart_Click);
            // 
            // buttonStop
            // 
            this.buttonStop.Enabled = false;
            this.buttonStop.Location = new System.Drawing.Point(139, 129);
            this.buttonStop.Name = "buttonStop";
            this.buttonStop.Size = new System.Drawing.Size(75, 23);
            this.buttonStop.TabIndex = 13;
            this.buttonStop.Text = "Stop";
            this.buttonStop.UseVisualStyleBackColor = true;
            this.buttonStop.Click += new System.EventHandler(this.buttonStop_Click);
            // 
            // serialPort1
            // 
            this.serialPort1.BaudRate = 115200;
            this.serialPort1.PortName = "COM22";
            this.serialPort1.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.serialPort1_DataReceived);
            // 
            // numericUpDown_kp
            // 
            this.numericUpDown_kp.DecimalPlaces = 3;
            this.numericUpDown_kp.Increment = new decimal(new int[] {
            2,
            0,
            0,
            196608});
            this.numericUpDown_kp.Location = new System.Drawing.Point(60, 12);
            this.numericUpDown_kp.Name = "numericUpDown_kp";
            this.numericUpDown_kp.Size = new System.Drawing.Size(120, 20);
            this.numericUpDown_kp.TabIndex = 14;
            this.numericUpDown_kp.ValueChanged += new System.EventHandler(this.numericUpDown_kp_ValueChanged);
            // 
            // numericUpDown_kd
            // 
            this.numericUpDown_kd.DecimalPlaces = 3;
            this.numericUpDown_kd.Increment = new decimal(new int[] {
            1,
            0,
            0,
            131072});
            this.numericUpDown_kd.Location = new System.Drawing.Point(60, 38);
            this.numericUpDown_kd.Name = "numericUpDown_kd";
            this.numericUpDown_kd.Size = new System.Drawing.Size(120, 20);
            this.numericUpDown_kd.TabIndex = 15;
            this.numericUpDown_kd.ValueChanged += new System.EventHandler(this.numericUpDown_kd_ValueChanged);
            // 
            // numericUpDown_ki
            // 
            this.numericUpDown_ki.DecimalPlaces = 5;
            this.numericUpDown_ki.Increment = new decimal(new int[] {
            1,
            0,
            0,
            196608});
            this.numericUpDown_ki.Location = new System.Drawing.Point(60, 64);
            this.numericUpDown_ki.Name = "numericUpDown_ki";
            this.numericUpDown_ki.Size = new System.Drawing.Size(120, 20);
            this.numericUpDown_ki.TabIndex = 16;
            this.numericUpDown_ki.ValueChanged += new System.EventHandler(this.numericUpDown_ki_ValueChanged);
            // 
            // numericUpDown_angle
            // 
            this.numericUpDown_angle.Increment = new decimal(new int[] {
            90,
            0,
            0,
            0});
            this.numericUpDown_angle.Location = new System.Drawing.Point(60, 92);
            this.numericUpDown_angle.Maximum = new decimal(new int[] {
            360,
            0,
            0,
            0});
            this.numericUpDown_angle.Name = "numericUpDown_angle";
            this.numericUpDown_angle.Size = new System.Drawing.Size(120, 20);
            this.numericUpDown_angle.TabIndex = 17;
            this.numericUpDown_angle.ValueChanged += new System.EventHandler(this.numericUpDown_angle_ValueChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(235, 183);
            this.Controls.Add(this.numericUpDown_angle);
            this.Controls.Add(this.numericUpDown_ki);
            this.Controls.Add(this.numericUpDown_kd);
            this.Controls.Add(this.numericUpDown_kp);
            this.Controls.Add(this.buttonStop);
            this.Controls.Add(this.buttonStart);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Interface PID";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_kp)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_kd)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_ki)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_angle)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button buttonStart;
        private System.Windows.Forms.Button buttonStop;
        private System.IO.Ports.SerialPort serialPort1;
        private System.Windows.Forms.NumericUpDown numericUpDown_kp;
        private System.Windows.Forms.NumericUpDown numericUpDown_kd;
        private System.Windows.Forms.NumericUpDown numericUpDown_ki;
        private System.Windows.Forms.NumericUpDown numericUpDown_angle;
    }
}

