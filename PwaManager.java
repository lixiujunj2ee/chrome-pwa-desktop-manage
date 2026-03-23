import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class PwaManager extends JFrame {
    private final String BASE_PATH = System.getProperty("user.home") + "/.local/share/applications/";
    private DefaultListModel<String> listModel = new DefaultListModel<>();
    private JList<String> fileList = new JList<>(listModel);
    private JTextArea contentDisplay = new JTextArea();
    private JTextField searchInput = new JTextField();
    private JSplitPane splitPane; 
    private String currentSelectedFile = null;

    public PwaManager() {
        setTitle("PWA Manager");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setExtendedState(MAXIMIZED_BOTH);
        setLayout(new BorderLayout());

        // 加载图标
        try {
            java.net.URL iconURL = getClass().getResource("/icons/chrome-pwa-desktop-manage.png");
            if (iconURL != null) setIconImage(new ImageIcon(iconURL).getImage());
        } catch (Exception e) {}

        // 左侧：菜单
        JPanel left = new JPanel(new BorderLayout(10, 10));
        left.setBorder(new EmptyBorder(10, 10, 10, 10));
        left.setMinimumSize(new Dimension(400, 0)); // 确保最小宽度

        searchInput.setFont(new Font("SansSerif", Font.PLAIN, 22));
        searchInput.setBorder(BorderFactory.createTitledBorder("Search..."));
        searchInput.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent e) { filterFiles(); }
        });

        fileList.setFont(new Font("SansSerif", Font.PLAIN, 22));
        fileList.setFixedCellHeight(50);
        fileList.addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                String val = fileList.getSelectedValue();
                if (val != null) readFile(val);
            }
        });

        left.add(searchInput, BorderLayout.NORTH);
        left.add(new JScrollPane(fileList), BorderLayout.CENTER);

        // 右侧：内容
        JPanel right = new JPanel(new BorderLayout(10, 10));
        right.setBorder(new EmptyBorder(10, 10, 10, 10));

        contentDisplay.setFont(new Font("Monospaced", Font.PLAIN, 24));
        contentDisplay.setEditable(false);
        contentDisplay.setLineWrap(true);

        JPanel btns = new JPanel(new FlowLayout(FlowLayout.LEFT, 20, 10));
        Font f20 = new Font("SansSerif", Font.BOLD, 20);
        JButton b1 = new JButton("Add"); b1.setFont(f20);
        JButton b2 = new JButton("Icon"); b2.setFont(f20);
        JButton b3 = new JButton("Delete"); b3.setFont(f20);

        b1.addActionListener(e -> showAdd());
        b2.addActionListener(e -> showIcon());
        b3.addActionListener(e -> doDelete());

        btns.add(b1); btns.add(b2); btns.add(b3);
        right.add(new JScrollPane(contentDisplay), BorderLayout.CENTER);
        right.add(btns, BorderLayout.SOUTH);

        // 分割面板修复
        splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, left, right);
        splitPane.setDividerLocation(400); // 初始位置
        splitPane.setResizeWeight(0.0);    // 拉伸窗口时左侧不动
        add(splitPane, BorderLayout.CENTER);

        filterFiles();
    }

    private void filterFiles() {
        String q = searchInput.getText().toLowerCase();
        listModel.clear();
        File d = new File(BASE_PATH);
        if (d.exists()) {
            File[] fs = d.listFiles((dir, n) -> n.endsWith(".desktop"));
            if (fs != null) for (File f : fs) if (f.getName().toLowerCase().contains(q)) listModel.addElement(f.getName());
        }
    }

    private void readFile(String n) {
        currentSelectedFile = n;
        try { contentDisplay.setText(Files.readString(Paths.get(BASE_PATH, n))); } 
        catch (Exception e) { contentDisplay.setText("Error"); }
    }

    private void showAdd() {
        JTextField id = new JTextField(); JTextField nm = new JTextField(); JTextField fl = new JTextField();
        Object[] m = {"APP_ID:", id, "APP_NAME:", nm, "FILE_NAME:", fl};
        if (JOptionPane.showConfirmDialog(this, m, "Add", 2) == 0) runCmd("create", id.getText(), nm.getText(), fl.getText());
    }

    private void showIcon() {
        JTextField p = new JTextField(); JTextField id = new JTextField();
        Object[] m = {"PNG_PATH:", p, "APP_ID:", id};
        if (JOptionPane.showConfirmDialog(this, m, "Icon", 2) == 0) runCmd("icon", p.getText(), id.getText());
    }

    private void doDelete() {
        if (currentSelectedFile != null && JOptionPane.showConfirmDialog(this, "Delete?") == 0) {
            new File(BASE_PATH, currentSelectedFile).delete();
            filterFiles(); contentDisplay.setText("");
        }
    }

    private void runCmd(String... a) {
        new Thread(() -> {
            try {
                String p = System.getProperty("user.dir") + File.separator + "pwa";
                ArrayList<String> c = new ArrayList<>(); c.add(p); Collections.addAll(c, a);
                int code = new ProcessBuilder(c).start().waitFor();
                if (code == 0) SwingUtilities.invokeLater(this::filterFiles);
            } catch (Exception e) {}
        }).start();
    }

    public static void main(String[] args) {
        try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); } catch (Exception e) {}
        SwingUtilities.invokeLater(() -> {
            PwaManager m = new PwaManager();
            m.setVisible(true);
            // 解决 Linux 下初始化时左侧菜单被挤压的问题
            m.splitPane.setDividerLocation(500); 
        });
    }
}

